# @author  : Zhu ZhenDong
# @time    : 2023-06-15 01-39-27
# @function: State machine of the game
# @version : 0.1.0
from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from layouts.app_page import AppSharedMem, Communicator

import time
from abc import abstractmethod
import cv2

from core.Board import Board
from core.ArmCamera import DummyCamera
from core.ArmInterface import ArmInterface
from configs.config import *
from core.Detection import ChessBoardDetector
from core.Agent import Agent


DK_MOVING_CHESS_POS = "moving-chess-pos"
DK_BOARD = "chess-grid"
DK_ROBOT_PLAY_SIDE = "robot-side"


class StateMachine:
    def __init__(
        self,
        arm: ArmInterface,
        detector: ChessBoardDetector,
        camera: DummyCamera,
        agent: Agent,
        context: AppSharedMem,
        communicator: Communicator,
    ):
        self.current_state: Union[State, None] = None
        self.data = {
            DK_MOVING_CHESS_POS: None,
            DK_BOARD: None,
            DK_ROBOT_PLAY_SIDE: None,
        }
        self.arm = arm
        self.camera = camera
        self.detector = detector
        self.agent = agent

    def next_state(self):
        cmd = self.current_state.next_state_cmd
        self.current_state = self.current_state.link.get_end_state(cmd)


class State:
    DEFAULT_CMD = "State"

    def __init__(self, state_cmd: str, state_machine: StateMachine):
        self.state_cmd = state_cmd
        self.TAG = self.__class__.__str__(self)
        self.next_state_cmd: Union[State, None] = None
        self.link = Link(start_state=self)
        self.state_machine = state_machine
        self.arm = self.state_machine.arm

    def add_next_state(self, cmd: str, state):
        self.link.add_end_state(cmd, state)

    @abstractmethod
    def operation(self):
        """
        如果有下一个状态, 则必须在最后调用set_next_state, 设置为下一个状态的字符命令
        不要在这个函数里面写死循环, 执行完必须返回给上一层, 否则无法进入下一个状态
        """
        pass

    def set_next_state(self, state_cmd: str):
        self.next_state_cmd = state_cmd

    def set_global_data(self, key: str, val):
        self.state_machine.data[key] = val

    def display_next_states(self):
        print(self.link)

    def __str__(self):
        return self.state_cmd


class StartingState(State):
    DEFAULT_CMD = "start"

    def __init__(
        self,
        state_machine: StateMachine,
        state_cmd: str = DEFAULT_CMD,
        starting: bool = False,
    ):
        super().__init__(state_cmd, state_machine)
        self.state_machine = state_machine
        self.starting = starting

        if self.starting:
            self.state_machine.data[DK_ROBOT_PLAY_SIDE] = Board.P_RED
            self.next_state_cmd = ObserveState.DEFAULT_CMD
            print("INFO: Machine move first.")
        else:
            self.state_machine.data[DK_ROBOT_PLAY_SIDE] = Board.P_YELLOW
            self.next_state_cmd = WaitingPlayerState.DEFAULT_CMD
            print("INFO: Player move first.")

    def operation(self):
        if DEBUG:
            print(f"Entering state : {self.TAG}")

        self.arm.recovery()


class ObserveState(State):
    DEFAULT_CMD = "obs"

    def __init__(self, state_machine: StateMachine, state_cmd: str = DEFAULT_CMD):
        super().__init__(state_cmd, state_machine)

    def operation(self):
        if DEBUG:
            print(f"Entering state : {self.TAG}")

        self.arm.recovery()
        self.arm.observe_posture()
        print("INFO: Arm standing-by in observation position.")
        camera = self.state_machine.camera
        detector = self.state_machine.detector

        print("INFO: Starting recognition")
        # 循环读取相机帧
        while True:
            camera.update()
            frame = camera.get_frame()
            if frame is None:
                continue

            # 显示相机帧
            cv2.imshow("Main", frame)

            # 检测棋盘
            if detector.detect(frame):
                detector.update_stable_grid()
                print("INFO: Grid stabilized.")
                break

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()

        board = self.state_machine.detector.stable_board
        board.update()

        if board.done:
            self.next_state_cmd = OverState.DEFAULT_CMD
            return

        agent = self.state_machine.agent
        n = agent.plan_move(board)
        print(f"INFO: Next move {n}")

        self.set_global_data(DK_MOVING_CHESS_POS, n)
        self.next_state_cmd = MovingChessPieceState.DEFAULT_CMD


class MovingChessPieceState(State):
    DEFAULT_CMD = "moving"

    def __init__(self, state_machine: StateMachine, state_cmd: str = DEFAULT_CMD):
        super().__init__(state_cmd, state_machine)

    def operation(self):
        if DEBUG:
            print(f"Entering state : {self.TAG}")

        stable_board = self.state_machine.detector.stable_board
        watch_board = self.state_machine.detector.watch_board
        chess_n: Union[int, None] = self.state_machine.data[DK_MOVING_CHESS_POS]

        if not stable_board.is_n_valid(chess_n):
            raise Exception(f"Not valid move. Column {chess_n} is full.")

        self.arm.recovery()
        self.arm.hover_over_chessboard_n(chess_n)
        self.arm.drop_piece()
        print("INFO: Move complete.")
        watch_board.drop_piece(chess_n, self.state_machine.data[DK_ROBOT_PLAY_SIDE])
        stable_board.drop_piece(chess_n, self.state_machine.data[DK_ROBOT_PLAY_SIDE])
        print("INFO: Update detector board complete.")
        print("DEBUG: Now board status:")

        stable_board.update()
        if stable_board.done:
            self.next_state_cmd = OverState.DEFAULT_CMD
        else:
            self.next_state_cmd = WaitingPlayerState.DEFAULT_CMD


class WaitingPlayerState(State):
    DEFAULT_CMD = "wait"

    def __init__(self, state_machine: StateMachine, state_cmd: str = DEFAULT_CMD):
        super().__init__(state_cmd, state_machine)

    def operation(self):
        if DEBUG:
            print(f"Entering state : {self.TAG}")
            print("INFO: Waiting for grid change.")
        self.arm.recovery()
        self.arm.observe_posture()
        time.sleep(5)

        camera = self.state_machine.camera
        detector = self.state_machine.detector

        # 循环读取相机帧
        while True:
            camera.update()
            frame = camera.get_frame()
            if frame is None:
                continue

            # 显示相机帧
            cv2.imshow("Main", frame)

            # 检测棋盘
            self.state_machine.detector.detect(frame)
            if detector.is_grid_changed():
                print("INFO: Grid changed.")
                break

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()

        board = self.state_machine.detector.stable_board
        board.update()
        if board.done:
            self.next_state_cmd = OverState.DEFAULT_CMD
            return

        agent = self.state_machine.agent
        n = agent.plan_move(board)
        print(f"INFO: Next move {n}")

        self.set_global_data(DK_MOVING_CHESS_POS, n)
        self.next_state_cmd = MovingChessPieceState.DEFAULT_CMD


class OverState(State):
    DEFAULT_CMD = "over"

    def __init__(self, state_machine: StateMachine, state_cmd: str = DEFAULT_CMD):
        super().__init__(state_cmd, state_machine)

    def operation(self):
        self.state_machine.arm.recovery()
        board = self.state_machine.detector.stable_board
        if board.winner == 1:
            winner = "RED"
        else:
            winner = "YELLOW"
        print(f"Winner is {winner}")


class Link:
    def __init__(self, start_state: State = None, end_state: Dict[str, State] = None):
        self.start_state = start_state

        if end_state is None:
            self.end_state = {}
        else:
            self.end_state = end_state

    def get_end_state(self, cmd: str):
        if cmd in self.end_state.keys():
            return self.end_state[cmd]
        else:
            return None

    def add_end_state(self, command: str, state: State):
        self.end_state[command] = state
