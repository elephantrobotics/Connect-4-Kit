import numpy as np
from typing import Tuple
from core.logger import get_logger


class Board:
    # Constants for display
    DISPLAY_EMPTY = "O"
    DISPLAY_R = "R"
    DISPLAY_Y = "Y"

    # Constants for grid representation
    P_EMPTY = 0
    P_RED = 1
    P_YELLOW = 2

    def __init__(self):
        # Initialize board dimensions
        self.width = 7
        self.height = 6
        # Initialize empty grid
        self.grid = [
            [Board.P_EMPTY for j in range(self.height)] for i in range(self.width)
        ]
        # Initialize grids for red and yellow players
        self.grid_red = np.array(
            [[Board.P_EMPTY for j in range(self.height)] for i in range(self.width)],
            dtype=np.int8,
        )
        self.grid_yellow = np.array(
            [[Board.P_EMPTY for j in range(self.height)] for i in range(self.width)],
            dtype=np.int8,
        )
        # Initialize game status
        self.done = False
        self.winner = None
        self.draw = False
        self.valid = True
        self.last_drop_pos: Tuple[int, int] = None
        self.last_drop_color = None
        self.logger = get_logger(__name__)

    @classmethod
    def opponent(cls, player):
        # Return the opponent of the current player
        if player == Board.P_RED:
            return Board.P_YELLOW
        elif player == Board.P_YELLOW:
            return Board.P_RED

    def reset(self):
        # Reset the board to its initial state
        self.__init__()

    def display(self):
        """
        Display the board in text format
        """
        for y in range(6):
            for x in range(7):
                cell = self.grid[x][y]
                if cell == Board.P_RED:
                    print(Board.DISPLAY_R, end="")
                elif cell == Board.P_YELLOW:
                    print(Board.DISPLAY_Y, end="")
                else:
                    print(Board.DISPLAY_EMPTY, end="")
            print()
        print()

    def propagate_relative_grid(self):
        """
        Update the relative grids for red and yellow players based on the main grid
        The relative grid is defined such that the current player is always player 1 and the opponent is always player 2
        This is because the neural network only recognizes the current player as player 1
        """
        self.grid_red = np.array(self.grid)
        self.grid_yellow = np.array(self.grid)
        for x in range(self.width):
            for y in range(self.height):
                if self.grid_yellow[x][y] == Board.P_RED:
                    self.grid_yellow[x][y] = Board.P_YELLOW
                elif self.grid_yellow[x][y] == Board.P_YELLOW:
                    self.grid_yellow[x][y] = Board.P_RED

    def check_draw(self):
        for row in self.grid:
            for entry in row:
                if entry == Board.P_EMPTY:
                    return False
        return True

    def update_win_status(self):
        """
        Check if either player has won and update the game status accordingly
        """
        if self.check_player_x_win(self.P_RED):
            self.done = True
            self.winner = self.P_RED
        elif self.check_player_x_win(self.P_YELLOW):
            self.done = True
            self.winner = self.P_YELLOW
        elif self.check_draw():
            self.done = True
            self.winner = None
            self.draw = True

    def update(self):
        """
        Update the relative grids and the game status
        """
        self.propagate_relative_grid()
        self.update_win_status()

    def _check_symbol(self, player):
        """
        Return the symbol to check for a win condition based on the player
        """
        if player == self.P_RED:
            check = "1 1 1 1"
        else:
            check = "2 2 2 2"
        return check

    def _check_vertical_win(self, board_state, player):
        """
        Check for a vertical win condition
        """
        check = self._check_symbol(player)
        for j in range(self.height):
            if check in np.array_str(board_state[:, j]):
                return True
        return False

    def _check_horizontal_win(self, board_state, player):
        """
        Check for a horizontal win condition
        """
        check = self._check_symbol(player)
        for i in range(self.width):
            if check in np.array_str(board_state[i, :]):
                return True
        return False

    def _check_leading_diag(self, board_state, player):
        """
        Check for a win condition in the leading diagonals
        """
        check = self._check_symbol(player)
        for k in range(0, self.width - 4 + 1):
            left_diagonal = np.array(
                [
                    board_state[k + d, d]
                    for d in range(min(self.width - k, min(self.width, self.height)))
                ]
            )
            right_diagonal = np.array(
                [
                    board_state[d + k, self.height - d - 1]
                    for d in range(min(self.width - k, min(self.width, self.height)))
                ]
            )
            if check in np.array_str(left_diagonal) or check in np.array_str(
                right_diagonal
            ):
                return True
        return False

    def _check_counter_diag(self, board_state, player):
        """
        Check for a win condition in the counter diagonals
        """
        check = self._check_symbol(player)
        for k in range(1, self.height - 4 + 1):
            left_diagonal = np.array(
                [
                    board_state[d, d + k]
                    for d in range(min(self.height - k, min(self.width, self.height)))
                ]
            )
            right_diagonal = np.array(
                [
                    board_state[d, self.height - 1 - k - d]
                    for d in range(min(self.height - k, min(self.width, self.height)))
                ]
            )
            if check in np.array_str(left_diagonal) or check in np.array_str(
                right_diagonal
            ):
                return True
        return False

    def check_player_x_win(self, player):
        """
        Check if the given player has won
        """
        board_state = np.array(self.grid)
        if self._check_vertical_win(board_state, player):
            return True
        elif self._check_horizontal_win(board_state, player):
            return True
        elif self._check_leading_diag(board_state, player):
            return True
        elif self._check_counter_diag(board_state, player):
            return True
        return False

    def available_actions(self):
        """
        Return a list of available actions (columns where a piece can be dropped)
        """
        actions = []
        for x in range(self.width):
            if self.grid[x][0] == Board.P_EMPTY:
                actions.append(x)
        return actions

    def is_n_valid(self, x: int):
        """
        Check if a piece can be dropped in the given column
        """
        if self.grid[x][0] == Board.P_EMPTY:
            return True
        else:
            return False

    def available_cell_y(self, n: int) -> int:
        """
        Return the y-coordinate of the available cell in the given column
        """
        for y in range(self.height):
            if self.grid[n][y] != Board.P_EMPTY:
                return y - 1
        return self.height - 1

    @classmethod
    def grid_diff(cls, grid1, grid2):
        res = []
        for i in range(7):
            for j in range(6):
                if grid1[i][j] != grid2[i][j]:
                    res.append(((i, j), grid1[i][j], grid2[i][j]))
        return res

    def reset_last_state(self):
        self.last_drop_color = None
        self.last_drop_pos = None

    def drop_piece(self, x, player):
        """
        Drop a piece of the given player in the given column
        """
        if self.is_n_valid(x):
            y = self.available_cell_y(x)
            self.last_drop_pos = (x, y)
            self.last_drop_color = player
            self.grid[x][y] = player
            if player == Board.P_RED:
                self.grid_red[x][y] = self.P_RED
                self.grid_yellow[x][y] = self.P_YELLOW
            else:
                self.grid_red[x][y] = self.P_YELLOW
                self.grid_yellow[x][y] = self.P_RED
        else:
            raise Exception(f"Not valid move. Column {x} is full.")

    def check_board_state_valid(self):
        count_red = 0
        count_yellow = 0
        for row in self.grid:
            for entry in row:
                if entry == Board.P_RED:
                    count_red += 1
                elif entry == Board.P_YELLOW:
                    count_yellow += 1

        if abs(count_red - count_yellow) >= 2:
            return False
        else:
            return True

    def should_have_pieces(round) -> Tuple[int, int]:
        """Return how many red & yellow pieces should the board have when in round x

        Args:
            round (int): round number
        """
        if round % 2 == 0:
            return round // 2, round // 2 - 1
        else:
            return round // 2, round // 2


if __name__ == "__main__":

    def test_draw():
        def drop_layer0():
            board.drop_piece(0, Board.P_RED)
            board.drop_piece(1, Board.P_RED)
            board.drop_piece(2, Board.P_RED)
            board.drop_piece(3, Board.P_YELLOW)
            board.drop_piece(4, Board.P_RED)
            board.drop_piece(5, Board.P_RED)
            board.drop_piece(6, Board.P_RED)

        def drop_layer1():
            board.drop_piece(0, Board.P_YELLOW)
            board.drop_piece(1, Board.P_YELLOW)
            board.drop_piece(2, Board.P_YELLOW)
            board.drop_piece(3, Board.P_RED)
            board.drop_piece(4, Board.P_YELLOW)
            board.drop_piece(5, Board.P_YELLOW)
            board.drop_piece(6, Board.P_YELLOW)

        board = Board()
        for row in range(6):
            [drop_layer0, drop_layer1][row % 2]()

        # board.display()

        board.update()

        assert board.draw == True

        print("Draw test passed.")

    test_draw()
