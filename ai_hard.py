import random
from constants import BOARD_SIZE, AI_PLAYER, HUMAN_PLAYER
from ai_medium import AI_medium


class AI_hard:

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

    def is_extendable_three(self, board, ai_moves):
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
        for x, y in ai_moves:
            for dx, dy in directions:
                count = 1  # Start with 1 to count the current piece
                potential_blocks = []

                # Check in the positive direction
                for i in range(1, 4):
                    nx, ny = x + dx * i, y + dy * i
                    if (
                        0 <= nx < BOARD_SIZE
                        and 0 <= ny < BOARD_SIZE
                        and (nx, ny) in ai_moves
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
                        and (nx, ny) in ai_moves
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

                # Check if there is exactly one open end with at least two empty spaces in that direction
                if count == 3 and len(potential_blocks) == 1:
                    extendable_end = potential_blocks[0]
                    # Check if there's an additional empty space in the direction of the open end
                    next_x, next_y = extendable_end[0] + dx, extendable_end[1] + dy
                    if (
                        0 <= next_x < BOARD_SIZE
                        and 0 <= next_y < BOARD_SIZE
                        and board[next_x][next_y] == ""
                    ):
                        return True, extendable_end

        return False, None

    def evaluate_line(self, line, player):
        score = 0
        if line.count(player) == 5:
            score += 1000
        elif line.count(player) == 4 and line.count("") == 1:
            score += 100
        elif line.count(player) == 3 and line.count("") == 2:
            score += 10
        return score

    def evaluate_board(self):
        total_score = 0
        # Evaluate rows
        for row in self.board:
            for i in range(BOARD_SIZE - 4):
                line = row[i : i + 5]
                total_score += self.evaluate_line(line, AI_PLAYER)
                total_score -= self.evaluate_line(line, HUMAN_PLAYER)

        # Evaluate columns
        for col in range(BOARD_SIZE):
            for row in range(BOARD_SIZE - 4):
                line = [self.board[row + i][col] for i in range(5)]
                total_score += self.evaluate_line(line, AI_PLAYER)
                total_score -= self.evaluate_line(line, HUMAN_PLAYER)

        # Evaluate diagonals
        for row in range(BOARD_SIZE - 4):
            for col in range(BOARD_SIZE - 4):
                line = [self.board[row + i][col + i] for i in range(5)]
                total_score += self.evaluate_line(line, AI_PLAYER)
                total_score -= self.evaluate_line(line, HUMAN_PLAYER)

                line = [self.board[row + i][col + 4 - i] for i in range(5)]
                total_score += self.evaluate_line(line, AI_PLAYER)
                total_score -= self.evaluate_line(line, HUMAN_PLAYER)

        return total_score

    def get_dynamic_depth(self):
        empty_cells = sum(row.count("") for row in self.board)
        if empty_cells > (BOARD_SIZE**2) / 2:
            return 2  # Less depth in the early game
        elif empty_cells > (BOARD_SIZE**2) / 4:
            return 3  # Medium depth in the mid-game
        else:
            return 4  # More depth as the game progresses

    def get_possible_moves(self):
        moves = set()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == "":
                    # Check if the cell is near an existing stone
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            if (
                                0 <= i + di < BOARD_SIZE
                                and 0 <= j + dj < BOARD_SIZE
                                and self.board[i + di][j + dj] != ""
                            ):
                                moves.add((i, j))
                                break
        return list(moves)

    def check_unblocked_four(self, board, player_moves, player):
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
                count = 0  # Count of player's pieces in a row
                open_ends = 0  # Count of open ends around the line

                # Check the line in one direction
                for i in range(4):
                    nx, ny = x + dx * i, y + dy * i
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        if board[nx][ny] == player:
                            count += 1
                        elif board[nx][ny] == "":
                            if i == 0 or i == 3:  # Check only the ends for openness
                                open_ends += 1
                            break  # Stop if an empty space or opponent's piece is found
                        else:
                            break

                # Check the line in the opposite direction
                for i in range(1, 4):
                    nx, ny = x - dx * i, y - dy * i
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        if board[nx][ny] == player:
                            count += 1
                        elif board[nx][ny] == "":
                            if i == 3:
                                open_ends += 1
                            break
                        else:
                            break

                # Check if there is a four in a row with two open ends
                if count == 4 and open_ends == 2:
                    return True, (
                        x,
                        y,
                    )  # Return the coordinate which is part of the four in a row

        return False, None

    def minimax(self, depth, alpha, beta, is_maximizing):
        if depth == 0 or self.check_win(AI_PLAYER) or self.check_win(HUMAN_PLAYER):
            return self.evaluate_board()

        if is_maximizing:
            max_eval = -float("inf")
            for move in self.get_possible_moves():
                i, j = move
                self.board[i][j] = AI_PLAYER
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board[i][j] = ""
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in self.get_possible_moves():
                i, j = move
                self.board[i][j] = HUMAN_PLAYER
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board[i][j] = ""
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def move_hard(self):
        best_score = -float("inf")
        best_move = None
        depth = self.get_dynamic_depth()
        player_winning_next = False
        ai_extendable_three = False
        ai_winning_next = False

        # Check if the player or AI has a critical move
        for move in self.get_possible_moves():
            i, j = move

            self.board[i][j] = AI_PLAYER
            if self.check_win(AI_PLAYER):
                ai_winning_next = True
                best_move = (i, j)
            self.board[i][j] = ""

            if not ai_winning_next:
                if self.board[i][j] == "":
                    # Check if the player is about to win
                    self.board[i][j] = HUMAN_PLAYER
                    if self.check_win(HUMAN_PLAYER):
                        player_winning_next = True
                        best_move = (i, j)
                    self.board[i][j] = ""

            # Check if AI can extend a three in a row
            if not player_winning_next:
                ai_extendable_three, het_position = self.is_extendable_three(
                    self.board, self.ai_moves
                )
            if ai_extendable_three and not player_winning_next:

                best_move = het_position
            self.board[i][j] = ""

            if player_winning_next or ai_extendable_three:
                break

        if not player_winning_next and not ai_extendable_three:
            # Check if the player has a three in a row that needs to be blocked
            has_three, block_position = AI_medium.check_three_in_a_row(
                self.board, self.player_moves, HUMAN_PLAYER
            )
            # Update needed here: let algotithm decide which position is better
            if has_three:
                choice = random.randint(0, 1)
                best_move = block_position[choice]
            else:
                # Check if player has a 2-space-1 combination, if yes, block it!
                has_irregular_four, block_position = self.check_unblocked_four(
                    self.board, self.player_moves, HUMAN_PLAYER
                )
                if has_irregular_four:
                    best_move = block_position

            # If no immediate block is necessary, proceed with minimax
            if not best_move:
                for move in self.get_possible_moves():
                    i, j = move
                    self.board[i][j] = AI_PLAYER
                    score = self.minimax(depth, -float("inf"), float("inf"), False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = move

        if best_move:
            self.board[best_move[0]][best_move[1]] = AI_PLAYER
            self.ai_moves.append(best_move)
            self.update_button(best_move[0], best_move[1])
            self.current_player = HUMAN_PLAYER
            self.check_ai_win()
