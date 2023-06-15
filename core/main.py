from StateMachine import *
from ArmInterface import ArmInterface

# 设置先手状态
ROBOT_PLAY_FIRST = False
if ROBOT_PLAY_FIRST:
    ROBOT_SIDE = Board.P_RED
else:
    ROBOT_SIDE = Board.P_YELLOW


# 初始化状态机
def init_states():
    global fsm
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
    return start_state


if __name__ == "__main__":
    arm = ArmInterface("COM5", 115200)
    camera = ArmCamera(1)
    detector = ChessBoardDetector(camera.mtx, camera.dist)
    agent = Agent(ROBOT_SIDE)
    fsm = StateMachine(arm, camera, detector, agent)

    starting_state = init_states()
    fsm.current_state = starting_state

    while fsm.current_state is not None:
        fsm.current_state.operation()
        fsm.detector.debug_display_chess_console()
        fsm.next_state()

    print("Done")
