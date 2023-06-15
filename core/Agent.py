import onnxruntime as ort
from config import AGENT_PATH
import random
import math
import numpy as np
from Board import Board

EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 2000


class Agent:
    def __init__(self, player_side):
        # self.device = torch.device("cpu")
        # self.policy_net = torch.jit.load(AGENT_PATH, map_location=self.device)
        self.policy_net = ort.InferenceSession(AGENT_PATH)
        # self.policy_net.eval()
        self.player_side = player_side
        self.training = False

    def model_predict(
        self, state: np.ndarray, available_actions: list, steps_done=None
    ):
        available_actions = np.array(available_actions)
        # batch and color channel
        state = np.array(state, dtype=np.float32)[np.newaxis, np.newaxis, ...]
        epsilon = random.random()
        if self.training:
            eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(
                -1 * steps_done / EPS_DECAY
            )
        else:
            eps_threshold = 0

        # follow epsilon-greedy policy
        if epsilon > eps_threshold:
            # action recommendations from policy net
            input_name = self.policy_net.get_inputs()[0].name
            r_actions = self.policy_net.run(None, {input_name: state})[0][0, :]
            state_action_values = np.array(
                [r_actions[action] for action in available_actions]
            )
            argmax_action = np.argmax(state_action_values)
            greedy_action = available_actions[argmax_action]
            return greedy_action
        else:
            return random.choice(available_actions)

    def plan_move(self, board: Board):
        state = np.array(board.grid)
        available_actions = board.available_actions()
        opponent_player = board.opponent(self.player_side)

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

        attempt_board = Board()
        for action in available_actions:
            attempt_board.grid = state.copy()
            attempt_board.propagate_relative_grid()
            attempt_board.drop_piece(action, opponent_player)
            if attempt_board.check_player_x_win(opponent_player):
                print(f"INFO: Opponent is about to win. Block {action} position.")
                return action

        return self.model_predict(state, available_actions)


def demo0(board: Board, agent1: Agent, agent2: Agent):
    board.reset()
    board.display()

    while not board.done:
        state = board.grid_red.copy()
        available_actions = board.available_actions()
        action = agent1.model_predict(state, available_actions)
        # trained agent's move is denoted by O
        board.drop_piece(action, Board.P_RED)
        board.display()

        board.update()
        if board.done:
            break

        state = board.grid_yellow.copy()
        available_actions = board.available_actions()
        action = agent1.model_predict(state, available_actions)
        # trained agent's move is denoted by O
        board.drop_piece(action, Board.P_YELLOW)
        board.display()

        board.update()
        if board.done:
            break


if __name__ == "__main__":
    agent1 = Agent(player_side=Board.P_RED)
    agent2 = Agent(player_side=Board.P_YELLOW)
    board = Board()
    demo0(board, agent1, agent2)
