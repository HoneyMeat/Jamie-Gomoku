import random
from constants import BOARD_SIZE, AI_PLAYER


class AI_easy:
    def __init__(self, board, update_button_callback, check_ai_win_callback):
        self.board = board
        self.update_button = update_button_callback
        self.check_ai_win = check_ai_win_callback
        self.ai_moves = []  # Keep track of AI moves if needed

    def move_easy(self):
        empty_cells = [
            (i, j)
            for i in range(BOARD_SIZE)
            for j in range(BOARD_SIZE)
            if self.board[i][j] == ""
        ]
        if empty_cells:
            row, column = random.choice(empty_cells)
            self.board[row][column] = AI_PLAYER
            self.ai_moves.append((row, column))  # Record AI's move
            self.update_button(row, column)
            self.check_ai_win()
