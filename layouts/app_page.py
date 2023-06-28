# @author  : Zhu ZhenDong
# @time    : 2023-06-15 11-41-42
# @function: This script contains the main classes and functions for the application.
# @version : 1.0

# Importing necessary libraries and modules
from collections.abc import Callable, Iterable, Mapping
import logging
import time
import sys
from typing import Any
import cv2
import numpy as np
import threading
from typing import *

from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject, Slot, Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QWidget, QLabel
from layouts.app_page_ui import Ui_AppPage

from libs.NormalCamera import NormalCamera
from libs.ArucoDetector import ArucoDetector
from libs.Utils import numpy_to_pixmap

from core.ArmInterface import ArmInterface
from core.Detection import ChessBoardDetector
from core.Agent import Agent
from core.StateMachine import StateMachine
from core.ArmCamera import DummyCamera
from core.StateMachine import *
from core.logger import get_logger

# Setting up logger
logger = get_logger(__name__, logging.DEBUG)

# Class for handling communication between different parts of the application
class Communicator(QObject):
    destroy = Signal()
    load_ui = Signal(str)
    curr_cam_index = Signal(int)
    cam_frame_update = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

# Class for shared memory across the application
class AppSharedMem:
    def __init__(self):
        # camera section
        self.camera_on_flag: bool = False
        self.curr_cam_index: Union[None, int] = None
        self.curr_frame: Union[None, np.ndarray] = None
        self.camera_params = np.load("configs/normal_cam_params.npz").values()

        # video feed section
        self.video_feed0_on = False
        self.video_feed1_on = False
        self.video_feed2_on = False
        self.video_feed3_on = False

        # game fsm configs
        self.game_running = False
        self.robot_first = False
        self.aruco_detect_frame: np.ndarray | None = None
        self.color_detect_frame: np.ndarray | None = None

        # arm
        self.arm: ArmInterface | None = None

# Class for handling camera operations in a separate thread
class CameraThread(threading.Thread):
    def __init__(self, cam_index: int, shared_memory: AppSharedMem, cam_signal: Signal):
        super().__init__()
        self.running_flag: bool = True
        self.cam_index: int = cam_index
        self.cam: NormalCamera | None = None
        self.cam_signal: Signal = cam_signal
        self.mem: AppSharedMem = shared_memory
        self.fps = 10
        self.tick = 1 / self.fps

    def run(self):
        self.cam = NormalCamera(cam_index=self.cam_index)
        try:
            while self.running_flag:
                frame = self.cam.raw_color_frame()
                if frame is None:
                    self.mem.curr_frame = None
                self.mem.curr_frame = frame
                self.cam_signal.emit()
                time.sleep(self.tick)
        except Exception as e:
            print(e)

# Class for handling game operations in a separate thread
class GameThread(threading.Thread):
    def __init__(self, context: AppSharedMem, communicator: Communicator) -> None:
        super().__init__()
        self.context: AppSharedMem = context
        self.commu: Communicator = communicator

        # Setting up the game state
        ROBOT_PLAY_FIRST = context.robot_first
        if ROBOT_PLAY_FIRST:
            ROBOT_SIDE = Board.P_RED
        else:
            ROBOT_SIDE = Board.P_YELLOW

        arm = self.context.arm
        camera = DummyCamera(self.context)

        mtx, dist = self.context.camera_params
        detector = ChessBoardDetector(mtx, dist)
        agent = Agent(ROBOT_SIDE)
        fsm = StateMachine(arm, detector, camera, agent, self.context, self.commu)

        # Initializing states
        start_state = StartingState(fsm, starting=ROBOT_PLAY_FIRST)
        observe_state = ObserveState(fsm)
        moving_state = MovingChessPieceState(fsm)
        waiting_state = WaitingPlayerState(fsm)
        over_state = OverState(fsm)

        start_state.add_next_state(WaitingPlayerState.DEFAULT_CMD, waiting_state)
        start_state.add_next_state(ObserveState.DEFAULT_CMD, observe_state)

        waiting_state.add_next_state(MovingChessPieceState.DEFAULT_CMD, moving_state)
        waiting_state.add_next_state(OverState.DEFAULT_CMD, over_state)

        observe_state.add_next_state(MovingChessPieceState.DEFAULT_CMD, moving_state)
        observe_state.add_next_state(OverState.DEFAULT_CMD, over_state)

        moving_state.add_next_state(WaitingPlayerState.DEFAULT_CMD, waiting_state)
        moving_state.add_next_state(OverState.DEFAULT_CMD, over_state)

        fsm.current_state = start_state

        self.fsm = fsm

    def run(self):
        if self.fsm.current_state is None:
            raise Exception("fsm must have a starting state.")

        try:
            while self.fsm.current_state is not None and self.context.game_running:
                self.fsm.current_state.operation()
                self.fsm.detector.debug_display_chess_console()
                self.fsm.next_state()
        except Exception as e:
            print(sys.exc_info())

# Main class for the application
class AppPage:
    def __init__(self):
        self._widget = QWidget()
        self.signals = Communicator(self._widget)
        self.shared_memory = AppSharedMem()
        self.aruco_detector: Union[ArucoDetector, None] = None
        self.init_aruco_detector()

        self.cam_thread: Union[CameraThread, None] = None
        self.game_thread: Union[GameThread, None] = None

        self.init_shared_mem()

    # Initialize shared memory
    def init_shared_mem(self):
        self.shared_memory.arm = ArmInterface("COM5", 115200)

    # Initialize Aruco detector
    def init_aruco_detector(self):
        camera_params = np.load("libs/normal_cam_params.npz")
        mtx, dist = camera_params["mtx"], camera_params["dist"]
        MARKER_SIZE = 22
        self.aruco_detector = ArucoDetector(mtx, dist, MARKER_SIZE)

    # Setup dynamic UI elements
    def setup_ui_dynamics(self):
        self.ui.label_video_feed0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_video_feed1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_video_feed2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_video_feed3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Function to change camera index
        def change_cam_index(cam_index):
            self.shared_memory.curr_cam_index = cam_index

        self.ui.combo_camera_selection.currentIndexChanged.connect(
            self.signals.curr_cam_index
        )
        self.signals.curr_cam_index.connect(change_cam_index)

        # Connect button to open camera
        self.ui.btn_start_camera.clicked.connect(self.open_camera)

        # Connect button to stop camera
        self.ui.btn_stop_camera.clicked.connect(self.stop_camera)

        # Connect signal to update video GUI
        self.signals.cam_frame_update.connect(self.update_image)

        # Function to turn on/off video0 feed
        def switch_video0(status):
            self.shared_memory.video_feed0_on = status
            if status == False:
                self.ui.label_video_feed0.setPixmap(QPixmap())

        self.ui.switch_video0_on.stateChanged.connect(switch_video0)

        # Function to turn on/off video1 feed
        def switch_video1(status):
            self.shared_memory.video_feed1_on = status
            if status == False:
                self.ui.label_video_feed1.setPixmap(QPixmap())

        self.ui.switch_video1_on.stateChanged.connect(switch_video1)

        # Function to turn on/off video2 feed
        def switch_video2(status):
            self.shared_memory.video_feed2_on = status
            if status == False:
                self.ui.label_video_feed2.setPixmap(QPixmap())

        self.ui.switch_video2_on.stateChanged.connect(switch_video2)

        # Function to turn on/off video3 feed
        def switch_video3(status):
            self.shared_memory.video_feed3_on = status
            if status == False:
                self.ui.label_video_feed3.setPixmap(QPixmap())

        self.ui.switch_video3_on.stateChanged.connect(switch_video3)

        # Function to change current algorithm
        @Slot()
        def change_alg_mode(alg_index):
            self.shared_memory.curr_alg_mode = self.ui.combo_algs.itemData(alg_index)
            print(self.shared_memory.curr_alg_mode)

        self.ui.combo_algs.currentIndexChanged.connect(change_alg_mode)

        # Function to start game
        @Slot()
        def start_game():
            logger.info("start game")
            if self.game_thread is not None:
                self.shared_memory.game_running = False
                del self.game_thread
                self.game_thread = None

            self.game_thread = GameThread(self.shared_memory, self.signals)
            self.shared_memory.game_running = True
            self.game_thread.start()

        self.ui.btn_start_game.clicked.connect(start_game)

        # Function to stop game
        @Slot()
        def stop_game():
            logger.info("stop game")
            if self.game_thread is None:
                return
            self.shared_memory.game_running = False
            self.shared_memory.curr_frame = None
            self.shared_memory.color_detect_frame = None
            self.shared_memory.aruco_detect_frame = None
            del self.game_thread
            self.game_thread = None

        self.ui.btn_stop_game.clicked.connect(stop_game)

    # Function to setup UI
    def setup_ui(self) -> QWidget:
        self.ui = Ui_AppPage()
        self.ui.setupUi(self._widget)
        self.setup_ui_dynamics()
        return self._widget

    # Function to open camera
    @Slot()
    def open_camera(self):
        cam_index = self.shared_memory.curr_cam_index

        self.ui.label_video_feed0.setPixmap(QPixmap())
        self._widget.update()

        if self.cam_thread is not None:
            self.cam_thread.running_flag = False

        self.cam_thread = CameraThread(
            cam_index, self.shared_memory, self.signals.cam_frame_update
        )
        self.cam_thread.start()

    # Function to stop camera
    @Slot()
    def stop_camera(self):
        self.cam_thread.running_flag = False
        self.ui.label_video_feed0.setPixmap(QPixmap())
        self.ui.label_video_feed1.setPixmap(QPixmap())
        self.ui.label_video_feed2.setPixmap(QPixmap())
        self.ui.label_video_feed3.setPixmap(QPixmap())

        self._widget.update()

    # Function to update image
    @Slot()
    def update_image(self):
        """
        Note that the frame given here is the original frame from the camera, not scaled.
        Some recognition algorithms use area determination, and scaling may cause the algorithm to fail.
        If scaling is needed, it can be done after converting to pixmap.
        """

        # Function to update specific video feed
        def setup_video_feed(video_label, local_frame, image_format):
            pixmap = numpy_to_pixmap(local_frame, image_format)
            display_label = video_label
            target_size = display_label.size()
            scaled_pixmap = pixmap.scaled(
                target_size, aspectMode=Qt.AspectRatioMode.KeepAspectRatio
            )
            video_label.setPixmap(scaled_pixmap)

        frame = self.shared_memory.curr_frame
        if frame is None:
            return

        if self.shared_memory.video_feed0_on:
            setup_video_feed(
                self.ui.label_video_feed0, frame, QImage.Format.Format_BGR888
            )

        if self.shared_memory.video_feed1_on:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            setup_video_feed(
                self.ui.label_video_feed1, gray_frame, QImage.Format.Format_Grayscale8
            )

        if (
            self.shared_memory.video_feed2_on
            and self.shared_memory.color_detect_frame is not None
        ):
            setup_video_feed(
                self.ui.label_video_feed2,
                self.shared_memory.color_detect_frame,
                QImage.Format.Format_BGR888,
            )

        if self.shared_memory.video_feed3_on:
            pass

    # Function to get widget
    def get_widget(self) -> QWidget:
        return self._widget

    # Function to terminate UI
    def terminate_ui(self) -> None:
        return
