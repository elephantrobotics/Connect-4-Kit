# @author  : Zhu ZhenDong
# @time    : 2023-06-15 01-39-27
# @function: State machine of the game
# @version : 0.1.0

# Importing necessary libraries and modules
from __future__ import annotations
from typing import *

# Checking for type checking
if TYPE_CHECKING:
    from layouts.app_page import AppSharedMem, Communicator

# Importing necessary modules
import time
from abc import abstractmethod
import cv2
import logging

# Importing necessary classes from different modules
from core.Board import Board
from core.ArmCamera import DummyCamera
from core.ArmInterface import ArmInterface
from configs.config import *
from core.Detection import ChessBoardDetector
from core.Agent import Agent
from core.logger import get_logger

# Defining constants
DK_MOVING_CHESS_POS = "moving-chess-pos"
DK_BOARD = "chess-grid"
DK_ROBOT_PLAY_SIDE = "robot-side"
DK_HUMAN_PLAY_SIDE = "human-side"

# Setting up logger
logger = get_logger(__name__)


# Defining the StateMachine class
class StateMachine:
    # Initializer method
    def __init__(
        self,
        arm: ArmInterface,
        detector: ChessBoardDetector,
        camera: DummyCamera,
        agent: Agent,
        context: AppSharedMem = None,
        communicator: Communicator = None,
    ):
        # Initializing class variables
        self.current_state: Union[State, None] = None
        self.data = {
            DK_MOVING_CHESS_POS: None,
            DK_BOARD: None,
            DK_ROBOT_PLAY_SIDE: None,
            DK_HUMAN_PLAY_SIDE: None,
        }
        self.arm = arm
        self.camera = camera
        self.detector = detector
        self.agent = agent
        self.context: AppSharedMem = context
        self.commu: Communicator = communicator
        self.winner = None
        self.robot_first = self.context.robot_first

    # Method to move to the next state
    def next_state(self):
        cmd = self.current_state.next_state_cmd
        self.current_state = self.current_state.link.get_end_state(cmd)


# Defining the State class
class State:
    DEFAULT_CMD = "State"

    # Initializer method
    def __init__(self, state_cmd: str, state_machine: StateMachine):
        self.state_cmd = state_cmd
        self.TAG = self.__class__.__str__(self)
        self.next_state_cmd: Union[State, None] = None
        self.link = Link(start_state=self)
        self.state_machine = state_machine
        self.arm = self.state_machine.arm

    # Method to add the next state
    def add_next_state(self, cmd: str, state):
        self.link.add_end_state(cmd, state)

    # Abstract method for operation
    @abstractmethod
    def operation(self):
        """
        如果有下一个状态, 则必须在最后调用set_next_state, 设置为下一个状态的字符命令
        不要在这个函数里面写死循环, 执行完必须返回给上一层, 否则无法进入下一个状态
        """
        pass

    # Method to set the next state
    def set_next_state(self, state_cmd: str):
        self.next_state_cmd = state_cmd

    # Method to set global data
    def set_global_data(self, key: str, val):
        self.state_machine.data[key] = val

    # Method to display the next states
    def display_next_states(self):
        print(self.link)

    # Method to convert the state to string
    def __str__(self):
        return self.state_cmd


# Defining the StartingState class
class StartingState(State):
    DEFAULT_CMD = "start"

    # Initializer method
    def __init__(
        self,
        state_machine: StateMachine,
        state_cmd: str = DEFAULT_CMD,
        starting: bool = False,
    ):
        super().__init__(state_cmd, state_machine)
        self.state_machine = state_machine
        self.starting = starting

        # Setting up the initial state
        if self.starting:
            self.state_machine.data[DK_ROBOT_PLAY_SIDE] = Board.P_RED
            self.state_machine.data[DK_HUMAN_PLAY_SIDE] = Board.P_YELLOW
            self.next_state_cmd = ObserveState.DEFAULT_CMD
            logger.info("INFO: Machine move first.")
        else:
            self.state_machine.data[DK_ROBOT_PLAY_SIDE] = Board.P_YELLOW
            self.state_machine.data[DK_ROBOT_PLAY_SIDE] = Board.P_RED
            self.next_state_cmd = WaitingPlayerState.DEFAULT_CMD
            logger.info("INFO: Player move first.")

    # Operation method
    def operation(self):
        if DEBUG:
            logger.info(f"Entering state : {self.TAG}")

        self.arm.recovery()


# Defining the ObserveState class
class ObserveState(State):
    DEFAULT_CMD = "obs"

    # Initializer method
    def __init__(self, state_machine: StateMachine, state_cmd: str = DEFAULT_CMD):
        super().__init__(state_cmd, state_machine)

    # Operation method
    def operation(self):
        if DEBUG:
            logger.info(f"Entering state : {self.TAG}")
        self.arm.recovery()
        self.arm.observe_posture()
        logger.info("INFO: Arm standing-by in observation position.")
        camera = self.state_machine.camera
        detector = self.state_machine.detector

        logger.info("INFO: Starting recognition")
        # 循环读取相机帧
        while self.state_machine.context.game_running:
            camera.update()
            frame = camera.get_frame()
            if frame is None:
                self.state_machine.context.color_detect_frame = None
                time.sleep(1 / FPS)
                continue

            rectified_frame = detector.rectify_frame(frame)
            if rectified_frame is None:
                self.state_machine.context.color_detect_frame = None
                time.sleep(1 / FPS)
                continue

            self.state_machine.context.color_detect_frame = detector.visu_chessboard(
                rectified_frame
            )

            # 检测棋盘
            if detector.detect(frame):
                logger.info("INFO: Grid stabilized.")

                # Check if piece difference is greater than 1
                if not detector.stable_board.check_board_state_valid():
                    logger.error("Board state invalid.")
                    self.state_machine.commu.stop_game.emit()

                if detector.stable_board.last_drop_pos is not None:
                    x, y = detector.stable_board.last_drop_pos
                    virtual_entry = detector.stable_board.last_drop_color
                    actual_entry = detector.stable_board.grid[x][y]
                    if actual_entry == virtual_entry:
                        logger.info("check position success")
                    else:
                        logger.error("check position failed")
                        continue

                break

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()

        board = self.state_machine.detector.stable_board
        board.update()

        if board.done:
            self.next_state_cmd = OverState.DEFAULT_CMD
            time.sleep(0.1)
            return

        agent = self.state_machine.agent
        n = agent.plan_move(board)
        logger.info(f"INFO: Next move {n}")

        self.set_global_data(DK_MOVING_CHESS_POS, n)
        self.next_state_cmd = MovingChessPieceState.DEFAULT_CMD


# Defining the MovingChessPieceState class
class MovingChessPieceState(State):
    DEFAULT_CMD = "moving"

    # Initializer method
    def __init__(self, state_machine: StateMachine, state_cmd: str = DEFAULT_CMD):
        super().__init__(state_cmd, state_machine)

    # Operation method
    def operation(self):
        if DEBUG:
            logger.info(f"Entering state : {self.TAG}")

        stable_board = self.state_machine.detector.stable_board
        watch_board = self.state_machine.detector.watch_board
        chess_n: Union[int, None] = self.state_machine.data[DK_MOVING_CHESS_POS]

        if not stable_board.is_n_valid(chess_n):
            raise Exception(f"Not valid move. Column {chess_n} is full.")

        self.arm.recovery()
        self.arm.hover_over_chessboard_n(chess_n)
        self.arm.drop_piece()
        logger.info("INFO: Move complete.")
        watch_board.drop_piece(chess_n, self.state_machine.data[DK_ROBOT_PLAY_SIDE])
        stable_board.drop_piece(chess_n, self.state_machine.data[DK_ROBOT_PLAY_SIDE])
        logger.info("INFO: Update detector board complete.")
        logger.info("DEBUG: Now board status:")

        stable_board.update()

        if stable_board.done:
            self.next_state_cmd = OverState.DEFAULT_CMD
        else:
            self.next_state_cmd = WaitingPlayerState.DEFAULT_CMD


# Defining the WaitingPlayerState class
class WaitingPlayerState(State):
    DEFAULT_CMD = "wait"

    # Initializer method
    def __init__(self, state_machine: StateMachine, state_cmd: str = DEFAULT_CMD):
        super().__init__(state_cmd, state_machine)

    # Operation method
    def operation(self):
        if DEBUG:
            logger.info(f"Entering state : {self.TAG}")
            logger.info("INFO: Waiting for grid change.")

        self.arm.recovery()
        self.arm.observe_posture()
        time.sleep(3)

        camera = self.state_machine.camera
        detector = self.state_machine.detector

        # 循环读取相机帧
        while self.state_machine.context.game_running:
            camera.update()
            frame = camera.get_frame()
            if frame is None:
                self.state_machine.context.color_detect_frame = None
                time.sleep(1 / FPS)
                continue

            rectified_frame = detector.rectify_frame(frame)
            if rectified_frame is None:
                self.state_machine.context.color_detect_frame = None
                time.sleep(1 / FPS)
                continue

            self.state_machine.context.color_detect_frame = detector.visu_chessboard(
                rectified_frame
            )

            if not detector.stable_board.check_board_state_valid():
                logger.error("Board state invalid.")
                self.state_machine.commu.stop_game.emit()

            # 检测棋盘
            self.state_machine.detector.detect(frame)
            if detector.is_grid_changed():
                logger.info("INFO: Grid changed.")

                if detector.stable_board.last_drop_pos is not None:
                    x, y = detector.stable_board.last_drop_pos
                    virtual_entry = detector.stable_board.last_drop_color
                    actual_entry = detector.stable_board.grid[x][y]
                    logger.info(f"virtual entry: {virtual_entry}")
                    logger.info(f"actual entry:{actual_entry}")
                    
                    detector.stable_board.reset_last_state()
                    detector.watch_board.reset_last_state()

                    if actual_entry == virtual_entry:
                        logger.info("check position success")
                        break
                    else:
                        diff = detector.change_diff
                        diff_robot = list(
                            filter(
                                lambda x: (x[0] != detector.stable_board.last_drop_pos)
                                and (
                                    x[2] == self.state_machine.data[DK_ROBOT_PLAY_SIDE]
                                ),
                                diff,
                            )
                        )
                        diff_human = list(
                            filter(
                                lambda x: (x[0] != detector.stable_board.last_drop_pos)
                                and (
                                    x[2] == self.state_machine.data[DK_HUMAN_PLAY_SIDE]
                                ),
                                diff,
                            )
                        )
                        logger.debug(f"diff:{diff}")
                        logger.error("robot drop position error.")

                        if len(diff_robot) == 1 and len(diff_human) == 1:
                            logger.warning("将错就错")
                            break
                        elif len(diff_robot) == 1 and len(diff_human) == 0:
                            logger.warning("将错就错且继续等待")
                            continue
                        elif len(diff_robot) == 0 and len(diff_human) == 0:
                            logger.warning("补救一下，重下一颗")
                            break
                        else:
                            logger.error("无法补救，终止对弈")
                            self.state_machine.commu.stop_game.emit()
                            self.state_machine.commu.info_msgbox.emit("对局出现错误，正在停止")

                break

        board = self.state_machine.detector.stable_board
        board.update()
        if board.done:
            self.next_state_cmd = OverState.DEFAULT_CMD
            return

        agent = self.state_machine.agent
        n = agent.plan_move(board)
        logger.info(f"INFO: Next move {n}")

        self.set_global_data(DK_MOVING_CHESS_POS, n)
        self.next_state_cmd = MovingChessPieceState.DEFAULT_CMD


# Defining the OverState class
class OverState(State):
    DEFAULT_CMD = "over"

    # Initializer method
    def __init__(self, state_machine: StateMachine, state_cmd: str = DEFAULT_CMD):
        super().__init__(state_cmd, state_machine)

    # Operation method
    def operation(self):
        self.state_machine.arm.recovery()
        board = self.state_machine.detector.stable_board
        if board.winner == 1:
            self.state_machine.winner = "RED"
        else:
            self.state_machine.winner = "YELLOW"
        logger.info(f"Winner is {self.state_machine.winner}")


# Defining the Link class
class Link:
    # Initializer method
    def __init__(self, start_state: State = None, end_state: Dict[str, State] = None):
        self.start_state = start_state

        if end_state is None:
            self.end_state = {}
        else:
            self.end_state = end_state

    # Method to get the end state
    def get_end_state(self, cmd: str):
        if cmd in self.end_state.keys():
            return self.end_state[cmd]
        else:
            return None

    # Method to add the end state
    def add_end_state(self, command: str, state: State):
        self.end_state[command] = state
