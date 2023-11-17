# Importing required modules
from core.StateMachine import *
from pymycobot import MyCobot, MyArm
from core.ArmInterface import ArmInterface, _MyArm, _MyCobot
from core.ArmCamera import ArmCamera
from serial.tools import list_ports
import numpy as np
import platform

# Setting the initial state of the game
# If ROBOT_PLAY_FIRST is True, the robot will play first, else the opponent will play first
ROBOT_PLAY_FIRST = False
if ROBOT_PLAY_FIRST:
    ROBOT_SIDE = Board.P_RED
else:
    ROBOT_SIDE = Board.P_YELLOW


# Function to initialize the states of the game
def init_states():
    # Declaring fsm as a global variable
    global fsm
    # Defining the initial states of the game
    start_state = StartingState(fsm, starting=ROBOT_PLAY_FIRST)
    observe_state = ObserveState(fsm)
    moving_state = MovingChessPieceState(fsm)
    waiting_state = WaitingPlayerState(fsm)
    over_state = OverState(fsm)

    # Adding next possible states for each state
    start_state.add_next_state(WaitingPlayerState.DEFAULT_CMD, waiting_state)
    start_state.add_next_state(ObserveState.DEFAULT_CMD, observe_state)

    waiting_state.add_next_state(MovingChessPieceState.DEFAULT_CMD, moving_state)
    waiting_state.add_next_state(OverState.DEFAULT_CMD, over_state)

    observe_state.add_next_state(MovingChessPieceState.DEFAULT_CMD, moving_state)
    observe_state.add_next_state(OverState.DEFAULT_CMD, over_state)

    moving_state.add_next_state(WaitingPlayerState.DEFAULT_CMD, waiting_state)
    moving_state.add_next_state(OverState.DEFAULT_CMD, over_state)
    # Returning the start state
    return start_state


def get_available_serial_port():
    return list(list_ports.comports())


def select_serial() -> str:
    print("Select a serial port (Enter the number):")

    while True:
        com_ports = get_available_serial_port()
        for i, port in enumerate(com_ports):
            print(f"({i}) - {port}")

        reply = input("Enter number of your select :")
        if str.isdigit(reply) and 0 <= int(reply) <= len(com_ports) - 1:
            device = com_ports[int(reply)].device
            return device

        print("Wrong number, try again.\n")

def select_robot_model():
    print("Select a robot model (Enter the number):")

    while True:
        print(f"(0) - MyCobot")
        print(f"(1) - MyArm")

        reply = input("Enter number of your select :")
        if reply == "0":
            return MyCobot
        elif reply == "1":
            return MyArm
        else:
            print("Wrong number, try again.\n")

# Class for shared memory across the application
class Context:
    def __init__(self):
        # camera section
        self.camera_on_flag: bool = False
        self.curr_cam_index: Union[None, int] = None
        self.curr_frame: Union[None, np.ndarray] = None
        self.camera_params = np.load("configs/normal_cam_params.npz").values()

        # game fsm configs
        self.game_running = False
        self.robot_first = False
        self.aruco_detect_frame: Union[np.ndarray, None] = None
        self.color_detect_frame: Union[np.ndarray, None] = None
        self.wait: Union[int , None] = None

        # arm
        self.arm: Union[ArmInterface , None] = None


# Main function
if __name__ == "__main__":
    robot_model = select_robot_model()
    serial_port = select_serial()
    cam_index = input("Please input camera index:")

    # Initializing the arm interface
    arm = None
    if robot_model == MyCobot:
        arm = _MyCobot(serial_port)
    elif robot_model == MyArm:
        arm = _MyArm(serial_port)
    
    # Initializing the camera
    camera = ArmCamera(int(cam_index))
    # Initializing the chess board detector
    detector = ChessBoardDetector(camera.mtx, camera.dist)
    # Initializing the agent
    agent = Agent(ROBOT_SIDE)
    # Initializing context
    context = Context()
    # Initializing the state machine
    fsm = StateMachine(arm,detector, camera, agent, context)
    # Setting the current state to the starting state
    starting_state = init_states()
    fsm.current_state = starting_state

    # Loop to keep the game running until there is a current state
    while fsm.current_state is not None:
        # Performing the operation of the current state
        fsm.current_state.operation()
        # Displaying the chess console for debugging
        fsm.detector.debug_display_chess_console()
        # Moving to the next state
        fsm.next_state()

    # Printing "Done" when the game is over
    print("Done")
