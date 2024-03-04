import tkinter as tk
from tkinter import messagebox, Menu, Label, Button
import random
import os

# Constants
BOARD_SIZE = 18
CELL_SIZE = 40
HUMAN_PLAYER = "X"
AI_PLAYER = "O"
SCORE_FILE = "game_scores.txt"


class Gomoku:
    def __init__(self, master, ai_difficulty):
        self.master = master
        self.ai_difficulty = ai_difficulty  # Set difficulty based on user selection
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = HUMAN_PLAYER
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.human_score = 0
        self.ai_score = 0
        self.move_count = 0
        self.player_moves = []  # List to store player's moves
        self.ai_moves = []  # List to store AI's moves
        self.lowest_round, self.highest_score = self.load_game_scores()
        self.initialize_board()
        self.initialize_scoreboard()
        self.initialize_menu()

    def initialize_board(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                button = tk.Button(
                    self.master,
                    width=2,
                    height=1,
                    command=lambda i=i, j=j: self.on_cell_clicked(i, j),
                )
                button.grid(row=i + 1, column=j)
                self.buttons[i][j] = button

    def initialize_scoreboard(self):
        self.score_label = tk.Label(self.master, text="", font=("Arial", 14))
        self.score_label.grid(row=0, column=0, columnspan=BOARD_SIZE)
        self.update_scoreboard()

    def initialize_menu(self):
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.difficulty_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(
            label=f"Difficulty: {self.ai_difficulty.capitalize()}", menu=self.difficulty_menu
        )

        self.difficulty_menu.add_command(label="Easy", command=lambda: self.set_difficulty("easy"))
        self.difficulty_menu.add_command(
            label="Medium", command=lambda: self.set_difficulty("medium")
        )
        self.difficulty_menu.add_command(label="Hard", command=lambda: self.set_difficulty("hard"))

    def set_difficulty(self, difficulty):
        self.ai_difficulty = difficulty
        # Update the menu label to show the current difficulty
        self.menu_bar.entryconfig(0, label=f"Difficulty: {self.ai_difficulty.capitalize()}")
        messagebox.showinfo(
            "Difficulty Set",
            f"AI difficulty set to {difficulty}. Restart the game to apply the changes.",
        )

    def update_scoreboard(self):
        score_text = f"Human (X): {self.human_score} | AI (O): {self.ai_score} | Highest Score: {self.highest_score} | Lowest Round: {self.lowest_round if self.lowest_round != float('inf') else 'N/A'}"
        self.score_label.config(text=score_text)

    def on_cell_clicked(self, row, column):
        if self.board[row][column] == "" and self.current_player == HUMAN_PLAYER:
            self.board[row][column] = HUMAN_PLAYER
            self.player_moves.append((row, column))  # Record player's move
            self.update_button(row, column)
            self.update_button(row, column)
            self.move_count += 1
            if self.check_win(HUMAN_PLAYER):
                messagebox.showinfo("Game Over", f"{HUMAN_PLAYER} wins!")
                self.human_score += 1
                self.update_game_scores()
                self.restart_game()
            else:
                self.current_player = AI_PLAYER
                self.ai_move()

    def update_button(self, row, column):
        self.buttons[row][column].config(text=self.board[row][column])

    def ai_move(self):
        # AI move logic based on the difficulty
        if self.ai_difficulty == "easy":
            self.ai_move_easy()
        elif self.ai_difficulty == "medium":
            self.ai_move_medium()
        else:  # self.ai_difficulty == "hard"
            self.ai_move_hard()
        self.current_player = HUMAN_PLAYER

    def ai_move_easy(self):
        empty_cells = [
            (i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j] == ""
        ]
        if empty_cells:
            row, column = random.choice(empty_cells)
            self.board[row][column] = AI_PLAYER
            self.ai_moves.append((row, column))  # Record AI's move
            self.update_button(row, column)
            self.check_ai_win()

    def ai_move_medium(self):
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
        has_three, block_position = self.check_three_in_a_row(self.player_moves, HUMAN_PLAYER)
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
        self.ai_move_easy()

    def check_three_in_a_row(self, player_moves, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]
        for x, y in player_moves:
            for dx, dy in directions:
                count = 1  # Start with 1 to count the current piece
                potential_blocks = []

                # Check in the positive direction
                for i in range(1, 4):
                    nx, ny = x + dx * i, y + dy * i
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and (nx, ny) in player_moves:
                        count += 1
                    else:
                        if (
                            0 <= nx < BOARD_SIZE
                            and 0 <= ny < BOARD_SIZE
                            and self.board[nx][ny] == ""
                        ):
                            potential_blocks.append((nx, ny))
                        break  # Break if encounter empty or opponent's piece

                # Check in the negative direction
                for i in range(1, 4):
                    nx, ny = x - dx * i, y - dy * i
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and (nx, ny) in player_moves:
                        count += 1
                    else:
                        if (
                            0 <= nx < BOARD_SIZE
                            and 0 <= ny < BOARD_SIZE
                            and self.board[nx][ny] == ""
                        ):
                            potential_blocks.insert(0, (nx, ny))  # Insert at the beginning
                        break  # Break if encounter empty or opponent's piece

                # Check if both ends are open for a valid three-in-a-row
                if count == 3 and len(potential_blocks) == 2:
                    return True, potential_blocks  # Both ends are open

        return False, None

    def is_near_player(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]
        for dx, dy in directions:
            if (
                0 <= x + dx < BOARD_SIZE
                and 0 <= y + dy < BOARD_SIZE
                and self.board[x + dx][y + dy] == HUMAN_PLAYER
            ):
                return True
        return False

    def is_extendable_three(self, i, j, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 0
            extendable = False
            for k in range(-1, 4):  # Check one beyond the line
                x, y = i + k * dx, j + k * dy
                if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                    if self.board[x][y] == player:
                        count += 1
                    elif self.board[x][y] == "" and (k == -1 or k == 3):
                        extendable = True
                    elif self.board[x][y] != player:
                        break
                if count == 3 and extendable:
                    return True
        return False

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

    def ai_move_hard(self):
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
                # Check if the player is about to win
                self.board[i][j] = HUMAN_PLAYER
                if self.check_win(HUMAN_PLAYER):
                    player_winning_next = True
                    best_move = (i, j)
                self.board[i][j] = ""

            # Check if AI can extend a three in a row
            if self.is_extendable_three(i, j, AI_PLAYER) and not player_winning_next:
                ai_extendable_three = True
                best_move = (i, j)
            self.board[i][j] = ""

            if player_winning_next or ai_extendable_three:
                break

        if not player_winning_next and not ai_extendable_three:
            # Check if the player has a three in a row that needs to be blocked
            has_three, block_position = self.check_three_in_a_row(self.player_moves, HUMAN_PLAYER)
            # Update needed here: let algotithm decide which position is better
            if has_three:
                choice = random.randint(0, 1)
                best_move = block_position[choice]

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

    def check_win(self, player):
        # Check horizontal, vertical, and diagonal win conditions
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.check_line_win(player, i, j):
                    return True
        return False

    def check_line_win(self, player, x, y):
        # Check if there's a line of five from (x, y)
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 0
            for i in range(5):
                if (
                    0 <= x + dx * i < BOARD_SIZE
                    and 0 <= y + dy * i < BOARD_SIZE
                    and self.board[x + dx * i][y + dy * i] == player
                ):
                    count += 1
                else:
                    break
            if count == 5:
                return True
        return False

    def restart_game(self):
        # Clear the board and reset the game
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.board[i][j] = ""
                self.buttons[i][j].config(text="", state="normal")
        self.current_player = HUMAN_PLAYER
        self.move_count = 0
        self.player_moves = []  # Clear the player's moves
        self.ai_moves = []  # Clear the AI's moves
        self.update_scoreboard()
        self.master.destroy()  # Close the current game window
        select_difficulty()  # Call the function to show the selection menu

    def load_game_scores(self):
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, "r") as file:
                scores = file.read().split(",")
                return int(scores[0]), int(scores[1])
        return float("inf"), 0  # Initialize lowest round to infinity and highest score to 0

    def update_game_scores(self):
        if self.move_count < self.lowest_round:
            self.lowest_round = self.move_count
        if self.human_score > self.highest_score:
            self.highest_score = self.human_score
        with open(SCORE_FILE, "w") as file:
            file.write(f"{self.lowest_round},{self.human_score}")
        self.update_scoreboard()

    def check_ai_win(self):
        if self.check_win(AI_PLAYER):
            messagebox.showinfo("Game Over", f"{AI_PLAYER} wins!")
            self.ai_score += 1
            self.update_game_scores()
            self.restart_game()


def select_difficulty():
    def set_difficulty_and_first_player(difficulty, first_player):
        selection_window.destroy()
        run_gomoku_game(difficulty, first_player)

    selection_window = tk.Tk()
    selection_window.title("Select Difficulty and First Player")

    Label(selection_window, text="Select Game Difficulty", font=("Arial", 16)).pack(pady=10)

    Button(
        selection_window,
        text="Easy - Player First",
        font=("Arial", 12),
        command=lambda: set_difficulty_and_first_player("easy", HUMAN_PLAYER),
    ).pack(fill="x", padx=50, pady=5)

    Button(
        selection_window,
        text="Easy - AI First",
        font=("Arial", 12),
        command=lambda: set_difficulty_and_first_player("easy", AI_PLAYER),
    ).pack(fill="x", padx=50, pady=5)

    Button(
        selection_window,
        text="Medium - Player First",
        font=("Arial", 12),
        command=lambda: set_difficulty_and_first_player("medium", HUMAN_PLAYER),
    ).pack(fill="x", padx=50, pady=5)

    Button(
        selection_window,
        text="Medium - AI First",
        font=("Arial", 12),
        command=lambda: set_difficulty_and_first_player("medium", AI_PLAYER),
    ).pack(fill="x", padx=50, pady=5)

    Button(
        selection_window,
        text="Hard - Player First",
        font=("Arial", 12),
        command=lambda: set_difficulty_and_first_player("hard", HUMAN_PLAYER),
    ).pack(fill="x", padx=50, pady=5)

    Button(
        selection_window,
        text="Hard - AI First",
        font=("Arial", 12),
        command=lambda: set_difficulty_and_first_player("hard", AI_PLAYER),
    ).pack(fill="x", padx=50, pady=5)

    # Repeat buttons for Medium and Hard difficulties with options for who goes first

    selection_window.mainloop()


def run_gomoku_game(difficulty, first_player):
    root = tk.Tk()
    root.title("Gomoku")
    game = Gomoku(root, difficulty)
    game.current_player = first_player
    if first_player == AI_PLAYER:
        # Place AI's first move in the center 3x3 area
        center = BOARD_SIZE // 2
        possible_moves = [(center + i, center + j) for i in range(-1, 2) for j in range(-1, 2)]
        move = random.choice(possible_moves)
        game.board[move[0]][move[1]] = AI_PLAYER
        game.ai_moves.append(move)
        game.update_button(move[0], move[1])
        game.current_player = HUMAN_PLAYER
    root.mainloop()


select_difficulty()
