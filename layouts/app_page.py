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
import serial
import platform

from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject, Slot, Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QMessageBox,
    QDialog,
    QBoxLayout,
)
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
logger = get_logger(__name__)


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
        self.wait: int | None = None

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

        self.cam = NormalCamera(cam_index=self.cam_index)
        logger.debug("Normal camera object created.")

        logger.debug(f"CameraThread instance {id(self)} created.")

    def run(self):
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

        logger.debug(f"GameThread {id(self)} created.")

    def run(self):
        if self.fsm.current_state is None:
            raise Exception("fsm must have a starting state.")

        logger.debug(f"GameThread {id(self)} running.")

        try:
            while self.fsm.current_state is not None and self.context.game_running:
                self.fsm.current_state.operation()
                self.fsm.detector.debug_display_chess_console()
                self.fsm.next_state()
        except Exception as e:
            print(sys.exc_info())


class SerialComboBox(QComboBox):
    # _res = Signal(dict)

    def __init__(self, parent):
        super(SerialComboBox, self).__init__(parent)

    def mousePressEvent(self, QMouseEvent):
        self.clear()
        serial_ports = serial.tools.list_ports.comports()
        for port in serial_ports:
            self.addItem(port.device)
        QComboBox.mousePressEvent(self, QMouseEvent)
        logger.debug("Serial port updated.")
        logger.debug(f"Now serial ports: {list(map(str,serial_ports))}")


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

        logger.debug("App Page created.")

    # Initialize Aruco detector
    def init_aruco_detector(self):
        camera_params = np.load("libs/normal_cam_params.npz")
        mtx, dist = camera_params["mtx"], camera_params["dist"]
        MARKER_SIZE = 22
        self.aruco_detector = ArucoDetector(mtx, dist, MARKER_SIZE)
        logger.debug("Aruco detector initialized.")

    # Setup dynamic UI elements
    def setup_ui_dynamics(self):
        self.ui.label_video_feed0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_video_feed1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_video_feed2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_video_feed3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Function to change camera index
        def change_cam_index(cam_index):
            self.shared_memory.curr_cam_index = cam_index
            logger.debug(f"Camera index changed to {cam_index}")

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

        def check_robot_first(state):
            if state:
                self.shared_memory.robot_first = True
            else:
                self.shared_memory.robot_first = False

        self.ui.check_robot_first.stateChanged.connect(check_robot_first)

        # Function to turn on/off video0 feed
        def switch_video0(status):
            self.shared_memory.video_feed0_on = status

            if status == False:
                self.ui.label_video_feed0.setPixmap(QPixmap())

            logger.debug(f"Video0 switched to {False if status == 0 else True}")

        self.ui.switch_video0_on.stateChanged.connect(switch_video0)

        # Function to turn on/off video1 feed
        def switch_video1(status):
            self.shared_memory.video_feed1_on = status
            if status == False:
                self.ui.label_video_feed1.setPixmap(QPixmap())
            logger.debug(f"Video1 switched to {False if status == 0 else True}")

        self.ui.switch_video1_on.stateChanged.connect(switch_video1)

        # Function to turn on/off video2 feed
        def switch_video2(status):
            self.shared_memory.video_feed2_on = status
            if status == False:
                self.ui.label_video_feed2.setPixmap(QPixmap())
            logger.debug(f"Video2 switched to {False if status == 0 else True}")

        self.ui.switch_video2_on.stateChanged.connect(switch_video2)

        # Function to turn on/off video3 feed
        def switch_video3(status):
            self.shared_memory.video_feed3_on = status
            if status == False:
                self.ui.label_video_feed3.setPixmap(QPixmap())
            logger.debug(f"Video3 switched to {False if status == 0 else True}")

        self.ui.switch_video3_on.stateChanged.connect(switch_video3)

        # Function to start game
        @Slot()
        def start_game():
            logger.debug("Start game button pressed.")
            if self.shared_memory.arm is None:
                QMessageBox.warning(None, QObject.tr("错误"), QObject.tr("请先连接机械臂"))
                return
            if self.cam_thread is None:
                QMessageBox.warning(None, QObject.tr("错误"), QObject.tr("请先连接相机"))
                return

            if self.game_thread is not None:
                self.shared_memory.game_running = False
                del self.game_thread
                self.game_thread = None

            self.game_thread = GameThread(self.shared_memory, self.signals)
            self.shared_memory.game_running = True
            self.game_thread.start()

            logger.debug("Game stared.")

        self.ui.btn_start_game.clicked.connect(start_game)

        # Function to stop game
        @Slot()
        def stop_game():
            logger.info("Stop game button pressed.")
            if self.game_thread is None:
                return

            self.shared_memory.game_running = False
            self.shared_memory.curr_frame = None
            self.shared_memory.color_detect_frame = None
            self.shared_memory.aruco_detect_frame = None

            # wait for threads to exit
            dialog = self.loading_dialog(QObject.tr("等待线程退出"))
            dialog.show()

            self.game_thread.join()

            dialog.close()

            del self.game_thread
            self.game_thread = None

            # clear ui
            self.shared_memory.curr_frame = None
            self.shared_memory.color_detect_frame = None
            self.shared_memory.aruco_detect_frame = None
            self.ui.label_video_feed2.setPixmap(QPixmap())
            logger.debug("Game stopped.")

        self.ui.btn_stop_game.clicked.connect(stop_game)

        # dynamically replace serial port select combox
        self.ui.combo_com_selection.deleteLater()
        self.ui.combo_com_selection = SerialComboBox(self.ui.frame_interact_panel)
        self.ui.horizontalLayout_18.addWidget(self.ui.combo_com_selection)

        @Slot()
        def connect_arm():
            logger.debug("Connect arm button pressed.")

            com_port = self.ui.combo_com_selection.currentText()
            if com_port is None:
                return

            system_name = platform.system().lower()
            if system_name == "windows":
                baud = 115200
            elif system_name == "linux":
                baud = 1000000
            else:
                logger.error(f"Platform {system_name} not supported")
                raise Exception("Platform {system_name} not supported")

            if com_port.startswith("COM") or com_port.startswith("/dev/ttyAMA"):
                self.shared_memory.arm = ArmInterface(com_port, baud)
                QMessageBox.information(None, QObject.tr("成功"), QObject.tr("机械臂连接成功"))
                logger.debug(f"Serial port {com_port} connected.")

            # TODO : add linux com port

        self.ui.btn_connect_com.clicked.connect(connect_arm)

        @Slot()
        def release_arm():
            logger.debug("Release arm button pressed.")

            # release before open
            if self.shared_memory.arm is None:
                return

            del self.shared_memory.arm
            self.shared_memory.arm = None
            QMessageBox.information(None, QObject.tr("成功"), QObject.tr("机械臂连接已关闭"))
            logger.debug("Arm released.")

        self.ui.btn_stop_com.clicked.connect(release_arm)

        @Slot()
        def btn_gservo():
            logger.debug("Drop piece button pressed.")

            if self.shared_memory.arm == None:
                QMessageBox.warning(None, QObject.tr("成功"), QObject.tr("请先连接机械臂"))

            self.shared_memory.arm.drop_piece()

        self.ui.btn_gservo.clicked.connect(btn_gservo)

    # Function to setup UI
    def setup_ui(self) -> QWidget:
        self.ui = Ui_AppPage()
        self.ui.setupUi(self._widget)
        self.setup_ui_dynamics()
        return self._widget

    # Function to open camera
    @Slot()
    def open_camera(self):
        # open before specify cam index
        if self.shared_memory.curr_cam_index is None:
            QMessageBox.warning(None, QObject.tr("错误"), QObject.tr("请先选择相机编号"))
            return

        cam_index = self.shared_memory.curr_cam_index

        self.ui.label_video_feed0.setPixmap(QPixmap())
        self._widget.update()

        if self.cam_thread is not None:
            self.cam_thread.running_flag = False

        dialog = self.loading_dialog(QObject.tr("等待相机启动"))
        dialog.show()

        self.cam_thread = CameraThread(
            cam_index, self.shared_memory, self.signals.cam_frame_update
        )

        dialog.close()

        self.cam_thread.start()
        self.ui.combo_camera_selection.setEnabled(False)

    # Function to stop camera
    @Slot()
    def stop_camera(self):
        # stop before start
        if self.cam_thread is None:
            return

        self.cam_thread.running_flag = False
        self.ui.label_video_feed0.setPixmap(QPixmap())
        self.ui.label_video_feed1.setPixmap(QPixmap())
        self.ui.label_video_feed2.setPixmap(QPixmap())
        self.ui.label_video_feed3.setPixmap(QPixmap())

        self.ui.combo_camera_selection.setEnabled(True)
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

    # Utility
    def loading_dialog(self, text):
        dialog = QDialog(self._widget)
        layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        layout.addWidget(QLabel(text))
        dialog.setLayout(layout)
        dialog.setWindowTitle(" ")
        # Disable close button
        dialog.setWindowFlag(Qt.WindowCloseButtonHint, False)

        return dialog

    def tr(self, text):
        # a = self._widget.tr("成功")
        a = QObject.tr(text)
        # a = QObject.tr("成功")
        return a
