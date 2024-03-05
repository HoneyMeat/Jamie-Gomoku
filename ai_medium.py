import random
from constants import BOARD_SIZE, AI_PLAYER, HUMAN_PLAYER


class AI_medium:
    def __init__(
        self,
        board,
        player_moves,
        update_button_callback,
        check_ai_win_callback,
        check_win_callback,
        easy_ai,
    ):
        self.board = board
        self.update_button = update_button_callback
        self.check_ai_win = check_ai_win_callback
        self.ai_moves = []  # Keep track of AI moves if needed
        self.check_win = check_win_callback
        self.player_moves = player_moves
        self.easy_ai = easy_ai

    def move_medium(self):
        # First, check if AI can win
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == "":
                    self.board[i][j] = AI_PLAYER
                    if self.check_win(AI_PLAYER):
                        self.update_button(i, j)
                        self.ai_moves.append((i, j))
                        self.check_ai_win()
                        return
                    self.board[i][j] = ""  # Undo the move

        # Then, block the player's immediate win
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == "":
                    self.board[i][j] = HUMAN_PLAYER
                    if self.check_win(HUMAN_PLAYER):
                        self.board[i][j] = AI_PLAYER
                        self.update_button(i, j)
                        self.ai_moves.append((i, j))
                        self.check_ai_win()
                        return
                    self.board[i][j] = ""  # Undo the move

        # Check and block the player's three in a row
        has_three, block_position = self.check_three_in_a_row(
            self.board, self.player_moves, HUMAN_PLAYER
        )
        if has_three:
            choice = random.randint(0, 1)
            i, j = block_position[choice]
            self.board[i][j] = AI_PLAYER
            self.update_button(i, j)
            self.ai_moves.append((i, j))
            self.check_ai_win()
            return

        # Place next to the player's stones if no immediate win or block is found
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == "" and self.is_near_player(i, j):
                    self.board[i][j] = AI_PLAYER
                    self.ai_moves.append((i, j))
                    self.update_button(i, j)
                    self.check_ai_win()
                    return

        # Fallback to a random move if no strategic move is found
        self.easy_ai.move_easy(self.board, self.ai_moves, self.update_button)

    @staticmethod
    def check_three_in_a_row(board, player_moves, player):
        directions = [
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1),
            (-1, 0),
            (0, -1),
            (-1, -1),
            (-1, 1),
        ]
        for x, y in player_moves:
            for dx, dy in directions:
                count = 1  # Start with 1 to count the current piece
                potential_blocks = []

                # Check in the positive direction
                for i in range(1, 4):
                    nx, ny = x + dx * i, y + dy * i
                    if (
                        0 <= nx < BOARD_SIZE
                        and 0 <= ny < BOARD_SIZE
                        and (nx, ny) in player_moves
                    ):
                        count += 1
                    else:
                        if (
                            0 <= nx < BOARD_SIZE
                            and 0 <= ny < BOARD_SIZE
                            and board[nx][ny] == ""
                        ):
                            potential_blocks.append((nx, ny))
                        break  # Break if encounter empty or opponent's piece

                # Check in the negative direction
                for i in range(1, 4):
                    nx, ny = x - dx * i, y - dy * i
                    if (
                        0 <= nx < BOARD_SIZE
                        and 0 <= ny < BOARD_SIZE
                        and (nx, ny) in player_moves
                    ):
                        count += 1
                    else:
                        if (
                            0 <= nx < BOARD_SIZE
                            and 0 <= ny < BOARD_SIZE
                            and board[nx][ny] == ""
                        ):
                            potential_blocks.insert(
                                0, (nx, ny)
                            )  # Insert at the beginning
                        break  # Break if encounter empty or opponent's piece

                # Check if both ends are open for a valid three-in-a-row
                if count == 3 and len(potential_blocks) == 2:
                    return True, potential_blocks  # Both ends are open

        return False, None

    def is_near_player(self, x, y):
        directions = [
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1),
            (-1, 0),
            (0, -1),
            (-1, -1),
            (-1, 1),
        ]
        for dx, dy in directions:
            if (
                0 <= x + dx < BOARD_SIZE
                and 0 <= y + dy < BOARD_SIZE
                and self.board[x + dx][y + dy] == HUMAN_PLAYER
            ):
                return True
        return False
