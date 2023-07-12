# Importing required modules
from core.StateMachine import *
from core.ArmInterface import ArmInterface
from core.ArmCamera import ArmCamera
from serial.tools import list_ports
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


# Main function
if __name__ == "__main__":
    os_name = platform.system().lower()

    if os_name == "windows":
        baud = 115200
    elif os_name == "linux":
        baud = 1000000
    else:
        raise Exception(f"Platform {os_name} is not supported.")

    serial_port = select_serial()

    # Initializing the arm interface
    arm = ArmInterface(serial_port, baud)
    # Initializing the camera
    camera = ArmCamera(1)
    # Initializing the chess board detector
    detector = ChessBoardDetector(camera.mtx, camera.dist)
    # Initializing the agent
    agent = Agent(ROBOT_SIDE)
    # Initializing the state machine
    fsm = StateMachine(arm, camera, detector, agent)

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
