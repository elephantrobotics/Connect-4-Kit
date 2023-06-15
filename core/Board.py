import numpy as np


class Board:
    # 用于在终端中显示的符号
    DISPLAY_EMPTY = "O"
    DISPLAY_R = "R"
    DISPLAY_Y = "Y"

    # 用于在grid内表示的符号
    P_EMPTY = 0
    P_RED = 1
    P_YELLOW = 2

    def __init__(self):
        self.width = 7
        self.height = 6
        self.grid = [[Board.P_EMPTY for j in range(self.height)] for i in range(self.width)]
        self.grid_red = np.array(
            [[Board.P_EMPTY for j in range(self.height)] for i in range(self.width)], dtype=np.int8)
        self.grid_yellow = np.array(
            [[Board.P_EMPTY for j in range(self.height)] for i in range(self.width)], dtype=np.int8)
        self.done = False
        self.winner = None

    @classmethod
    def opponent(cls, player):
        if player == Board.P_RED:
            return Board.P_YELLOW
        elif player == Board.P_YELLOW:
            return Board.P_RED

    def reset(self):
        self.__init__()

    def display(self):
        """
        用文字形式输出
        :return:
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
        通过主grid，更新相对红方和黄方的grid
        相对grid是指，看自己都是player1，看别人都是player2
        因为神经网络只知道自己是p1
        :return:
        """
        self.grid_red = np.array(self.grid)
        self.grid_yellow = np.array(self.grid)
        for x in range(self.width):
            for y in range(self.height):
                if self.grid_yellow[x][y] == Board.P_RED:
                    self.grid_yellow[x][y] = Board.P_YELLOW
                elif self.grid_yellow[x][y] == Board.P_YELLOW:
                    self.grid_yellow[x][y] = Board.P_RED

    def update_win_status(self):
        if self.check_player_x_win(self.P_RED):
            self.done = True
            self.winner = self.P_RED
        elif self.check_player_x_win(self.P_YELLOW):
            self.done = True
            self.winner = self.P_YELLOW

    def update(self):
        self.propagate_relative_grid()
        self.update_win_status()

    def _check_symbol(self, player):
        if player == self.P_RED:
            check = '1 1 1 1'
        else:
            check = '2 2 2 2'
        return check

    def _check_vertical_win(self, board_state, player):
        check = self._check_symbol(player)
        # check vertically then horizontally
        for j in range(self.height):
            if check in np.array_str(board_state[:, j]):
                return True
        return False

    def _check_horizontal_win(self, board_state, player):
        check = self._check_symbol(player)
        for i in range(self.width):
            if check in np.array_str(board_state[i, :]):
                return True
        return False

    def _check_leading_diag(self, board_state, player):
        check = self._check_symbol(player)
        # check left diagonal and right diagonal
        for k in range(0, self.width - 4 + 1):
            left_diagonal = np.array([board_state[k + d, d] for d in \
                                      range(min(self.width - k,
                                                min(self.width, self.height)))])
            right_diagonal = np.array([board_state[d + k, self.height - d - 1] for d in \
                                       range(min(self.width - k,
                                                 min(self.width, self.height)))])
            if check in np.array_str(left_diagonal) or check in np.array_str(right_diagonal):
                print("counter diag")
                return True
        return False

    def _check_counter_diag(self, board_state, player):
        check = self._check_symbol(player)
        for k in range(1, self.height - 4 + 1):
            left_diagonal = np.array([board_state[d, d + k] for d in \
                                      range(min(self.height - k,
                                                min(self.width, self.height)))])
            right_diagonal = np.array([board_state[d, self.height - 1 - k - d] for d in \
                                       range(min(self.height - k,
                                                 min(self.width, self.height)))])
            if check in np.array_str(left_diagonal) or check in np.array_str(right_diagonal):
                print("leading diag")
                return True
        return False

    def check_player_x_win(self, player):
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
        actions = []
        for x in range(self.width):
            if self.grid[x][0] == Board.P_EMPTY:
                actions.append(x)
        return actions

    def is_n_valid(self, x: int):
        if self.grid[x][0] == Board.P_EMPTY:
            return True
        else:
            return False

    def available_cell_y(self, n: int) -> int:
        """
        返回第n列的可用单元的y轴坐标
        :param n:
        :return:
        """
        for y in range(self.height):
            if self.grid[n][y] != Board.P_EMPTY:
                return y - 1
        return self.height - 1

    def drop_piece(self, x, player):
        if self.is_n_valid(x):
            y = self.available_cell_y(x)
            self.grid[x][y] = player
            if player == Board.P_RED:
                self.grid_red[x][y] = self.P_RED
                self.grid_yellow[x][y] = self.P_YELLOW
            else:
                self.grid_red[x][y] = self.P_YELLOW
                self.grid_yellow[x][y] = self.P_RED
        else:
            raise Exception(f"Not valid move. Column {x} is full.")
