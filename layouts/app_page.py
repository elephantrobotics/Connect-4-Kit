# @author  : Zhu ZhenDong
# @time    : 2023-06-15 11-41-42
# @function:
# @version :

import logging
import time
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


logger = logging.getLogger(__name__)


class Communicator(QObject):
    destroy = Signal()
    load_ui = Signal(str)
    curr_cam_index = Signal(int)
    cam_frame_update = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)


class AppSharedMem:
    def __init__(self):
        # camera section
        self.camera_on_flag: bool = False
        self.curr_cam_index: Union[None, int] = None
        self.curr_frame: Union[None, np.ndarray] = None

        # video feed section
        self.video_feed0_on = False
        self.video_feed1_on = False
        self.video_feed2_on = False
        self.video_feed3_on = False

        # game fsm configs


class CameraThread(threading.Thread):
    def __init__(self, cam_index: int, shared_memory: AppSharedMem, cam_signal: Signal):
        super().__init__()
        self.running_flag: bool = True
        self.cam_index: int = cam_index
        self.cam: NormalCamera | None = None
        self.cam_signal: Signal = cam_signal
        self.mem: AppSharedMem = shared_memory
        self.fps = 21
        self.tick = 1 / self.fps

    def run(self):
        self.cam = NormalCamera(cam_index=self.cam_index)
        try:
            while self.running_flag:
                frame = self.cam.raw_color_frame()
                self.mem.curr_frame = frame
                self.cam_signal.emit()
                time.sleep(self.tick)
        except Exception as e:
            print(e)


class AppPage:
    def __init__(self):
        self._widget = QWidget()
        self.signals = Communicator(self._widget)
        self.shared_memory = AppSharedMem()
        self.cam_thread: Union[CameraThread, None] = None
        self.aruco_detector: Union[ArucoDetector, None] = None
        self.init_aruco_detector()
        self.game_fsm = self.build_fsm()

    def build_fsm(self):
        # 设置先手状态
        ROBOT_PLAY_FIRST = False
        if ROBOT_PLAY_FIRST:
            ROBOT_SIDE = Board.P_RED
        else:
            ROBOT_SIDE = Board.P_YELLOW

        ROBOT_PLAY_FIRST = 1
        arm = ArmInterface("COM5", 115200)
        camera = DummyCamera(1)
        camera_params = np.load("configs/normal_cam_params.npz")
        mtx, dist = camera_params["mtx"], camera_params["dist"]
        detector = ChessBoardDetector(mtx, dist)
        agent = Agent(ROBOT_SIDE)
        fsm = StateMachine(
            arm, camera, detector, agent, self.shared_memory, self.signals
        )

        # init states
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

        return fsm

    def init_aruco_detector(self):
        camera_params = np.load("libs/normal_cam_params.npz")
        mtx, dist = camera_params["mtx"], camera_params["dist"]
        MARKER_SIZE = 22
        self.aruco_detector = ArucoDetector(mtx, dist, MARKER_SIZE)

    def setup_ui_dynamics(self):
        self.ui.label_video_feed0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_video_feed1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_video_feed2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_video_feed3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # change camera index
        def change_cam_index(cam_index):
            self.shared_memory.curr_cam_index = cam_index

        self.ui.combo_camera_selection.currentIndexChanged.connect(
            self.signals.curr_cam_index
        )
        self.signals.curr_cam_index.connect(change_cam_index)

        # open camera
        self.ui.btn_start_camera.clicked.connect(self.open_camera)

        # stop camera
        self.ui.btn_stop_camera.clicked.connect(self.stop_camera)

        # update video gui
        self.signals.cam_frame_update.connect(self.update_image)

        # turn on/off video0 feed
        def switch_video0(status):
            self.shared_memory.video_feed0_on = status
            if status == False:
                self.ui.label_video_feed0.setPixmap(QPixmap())

        self.ui.switch_video0_on.stateChanged.connect(switch_video0)

        # turn on/off video1 feed
        def switch_video1(status):
            self.shared_memory.video_feed1_on = status
            if status == False:
                self.ui.label_video_feed1.setPixmap(QPixmap())

        self.ui.switch_video1_on.stateChanged.connect(switch_video1)

        # turn on/off video2 feed
        def switch_video2(status):
            self.shared_memory.video_feed2_on = status
            if status == False:
                self.ui.label_video_feed2.setPixmap(QPixmap())

        self.ui.switch_video2_on.stateChanged.connect(switch_video2)

        # turn on/off video3 feed
        def switch_video3(status):
            self.shared_memory.video_feed3_on = status
            if status == False:
                self.ui.label_video_feed3.setPixmap(QPixmap())

        self.ui.switch_video3_on.stateChanged.connect(switch_video3)

        # change current algorithm
        @Slot()
        def change_alg_mode(alg_index):
            self.shared_memory.curr_alg_mode = self.ui.combo_algs.itemData(alg_index)
            print(self.shared_memory.curr_alg_mode)

        self.ui.combo_algs.currentIndexChanged.connect(change_alg_mode)

        # start play
        self.ui.btn_start_game.clicked.connect(self.start_game)

        # stop play
        self.ui.btn_stop_game.clicked.connect(self.stop_game)

    # 1.
    def setup_ui(self) -> QWidget:
        self.ui = Ui_AppPage()
        self.ui.setupUi(self._widget)
        self.setup_ui_dynamics()
        return self._widget

    @Slot()
    def start_game():
        pass

    @Slot()
    def stop_game():
        pass

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

    @Slot()
    def stop_camera(self):
        self.cam_thread.running_flag = False
        self.ui.label_video_feed0.setPixmap(QPixmap())
        self.ui.label_video_feed1.setPixmap(QPixmap())
        self._widget.update()

    @Slot()
    def start_game(self):
        pass

    @Slot()
    def stop_game(self):
        pass

    @Slot()
    def update_image(self):
        """
        需要注意的是, 这里给出的frame都是相机原始帧, 不经过scale
        因为部分识别算法使用的是面积判定, scale之后可能导致算法出错
        如果需要scale的话, 可以在转换成pixmap以后做
        """

        # update specific video feed
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

    # 2.
    def get_widget(self) -> QWidget:
        return self._widget

    # 3.
    def terminate_ui(self) -> None:
        return
