import tkinter as tk
from tkinter import messagebox, Menu
from constants import *
from utils import update_game_scores, load_game_scores
from ai_easy import AI_easy
from ai_medium import AI_medium
from ai_hard import AI_hard


class Gomoku:
    def __init__(self, master, ai_difficulty, on_restart):
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
        self.lowest_round, self.highest_score = load_game_scores()
        self.easy_ai = AI_easy(self.board, self.update_button, self.check_ai_win)
        self.medium_ai = AI_medium(
            self.board,
            self.player_moves,
            self.update_button,
            self.check_ai_win,
            self.check_win,
            self.easy_ai,
        )
        self.hard_ai = AI_hard(
            self.board,
            self.player_moves,
            self.update_button,
            self.check_ai_win,
            self.check_win,
            self.easy_ai,
        )
        self.on_restart = on_restart
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
            label=f"Difficulty: {self.ai_difficulty.capitalize()}",
            menu=self.difficulty_menu,
        )

        self.difficulty_menu.add_command(
            label="Easy", command=lambda: self.set_difficulty("easy")
        )
        self.difficulty_menu.add_command(
            label="Medium", command=lambda: self.set_difficulty("medium")
        )
        self.difficulty_menu.add_command(
            label="Hard", command=lambda: self.set_difficulty("hard")
        )

    def set_difficulty(self, difficulty):
        self.ai_difficulty = difficulty
        # Update the menu label to show the current difficulty
        self.menu_bar.entryconfig(
            0, label=f"Difficulty: {self.ai_difficulty.capitalize()}"
        )
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
                update_game_scores(self)
                self.restart_game()
            else:
                self.current_player = AI_PLAYER
                self.ai_move()

    def update_button(self, row, column):
        self.buttons[row][column].config(text=self.board[row][column])

    def ai_move(self):
        # AI move logic based on the difficulty
        if self.ai_difficulty == "easy":
            self.easy_ai.move_easy()  # Use the existing instance
        elif self.ai_difficulty == "medium":
            self.medium_ai.move_medium()
        else:  # self.ai_difficulty == "hard"
            self.hard_ai.move_hard()
        self.current_player = HUMAN_PLAYER

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
        self.on_restart()  # Call the function to show the selection menu

    def check_ai_win(self):
        if self.check_win(AI_PLAYER):
            messagebox.showinfo("Game Over", f"{AI_PLAYER} wins!")
            self.ai_score += 1
            update_game_scores(self)
            self.restart_game()
