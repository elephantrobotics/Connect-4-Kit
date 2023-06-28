# @author  : Zhu ZhenDong
# @time    : 2023-06-15 02-05-59
# @function: Agent that play chess with player
# @version :


# Import necessary libraries and modules
import onnxruntime as ort
from configs.config import AGENT_PATH
import random
import math
import numpy as np
from core.Board import Board

# Define constants for epsilon-greedy policy
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 2000

# Define the Agent class
class Agent:
    # Initialize the agent with a player side and a policy network
    def __init__(self, player_side):
        self.policy_net = ort.InferenceSession(AGENT_PATH)
        self.player_side = player_side
        self.training = False

    # Define the model prediction method
    def model_predict(
        self, state: np.ndarray, available_actions: list, steps_done=None
    ):
        # Convert available actions to numpy array
        available_actions = np.array(available_actions)
        # Add batch and color channel dimensions to state
        state = np.array(state, dtype=np.float32)[np.newaxis, np.newaxis, ...]
        # Generate a random number for epsilon-greedy policy
        epsilon = random.random()
        # Calculate epsilon threshold based on whether the agent is training or not
        if self.training:
            eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(
                -1 * steps_done / EPS_DECAY
            )
        else:
            eps_threshold = 0

        # Follow epsilon-greedy policy
        if epsilon > eps_threshold:
            # Get action recommendations from policy network
            input_name = self.policy_net.get_inputs()[0].name
            r_actions = self.policy_net.run(None, {input_name: state})[0][0, :]
            # Get state-action values for available actions
            state_action_values = np.array(
                [r_actions[action] for action in available_actions]
            )
            # Get the action with the highest state-action value
            argmax_action = np.argmax(state_action_values)
            greedy_action = available_actions[argmax_action]
            return greedy_action
        else:
            # Choose a random action
            return random.choice(available_actions)

    # Define the method for planning a move
    def plan_move(self, board: Board):
        # Get the current state and available actions
        state = np.array(board.grid)
        available_actions = board.available_actions()
        # Get the opponent player
        opponent_player = board.opponent(self.player_side)

        # Try each available action and check if it leads to a win
        attempt_board = Board()
        for action in available_actions:
            attempt_board.grid = state.copy()
            attempt_board.propagate_relative_grid()
            attempt_board.drop_piece(action, self.player_side)
            if attempt_board.check_player_x_win(self.player_side):
                print(
                    f"INFO: We are winning. Override model prediction and use {action} move."
                )
                return action

        # Try each available action and check if it prevents the opponent from winning
        attempt_board = Board()
        for action in available_actions:
            attempt_board.grid = state.copy()
            attempt_board.propagate_relative_grid()
            attempt_board.drop_piece(action, opponent_player)
            if attempt_board.check_player_x_win(opponent_player):
                print(f"INFO: Opponent is about to win. Block {action} position.")
                return action

        # If no winning or blocking move is found, use the model to predict the next move
        return self.model_predict(state, available_actions)

# Define the demo function
def demo0(board: Board, agent1: Agent, agent2: Agent):
    # Reset and display the board
    board.reset()
    board.display()

    # Play the game until it's done
    while not board.done:
        # Get the current state and available actions
        state = board.grid_red.copy()
        available_actions = board.available_actions()
        # Get the agent's move
        action = agent1.model_predict(state, available_actions)
        # Make the move and display the board
        board.drop_piece(action, Board.P_RED)
        board.display()

        # Update the board and check if the game is done
        board.update()
        if board.done:
            break

        # Repeat the process for the second agent
        state = board.grid_yellow.copy()
        available_actions = board.available_actions()
        action = agent1.model_predict(state, available_actions)
        board.drop_piece(action, Board.P_YELLOW)
        board.display()

        board.update()
        if board.done:
            break

# Define the main function
if __name__ == "__main__":
    # Create two agents and a board
    agent1 = Agent(player_side=Board.P_RED)
    agent2 = Agent(player_side=Board.P_YELLOW)
    board = Board()
    # Run the demo function
    demo0(board, agent1, agent2)