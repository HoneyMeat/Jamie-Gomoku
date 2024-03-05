import tkinter as tk
from tkinter import Label, Button
from game import Gomoku
from constants import HUMAN_PLAYER, AI_PLAYER, BOARD_SIZE
import random


def run_gomoku_game(difficulty, first_player):
    root = tk.Tk()
    root.title("Gomoku")
    game = Gomoku(root, ai_difficulty=difficulty, on_restart=select_difficulty)
    if first_player == AI_PLAYER:
        # AI makes the first move
        center = BOARD_SIZE // 2
        possible_moves = [
            (center + i, center + j) for i in range(-1, 2) for j in range(-1, 2)
        ]
        move = random.choice(possible_moves)
        game.board[move[0]][move[1]] = AI_PLAYER
        game.ai_moves.append(move)
        game.update_button(move[0], move[1])
    game.current_player = first_player
    root.mainloop()


def select_difficulty():
    def set_difficulty_and_first_player(difficulty, first_player):
        selection_window.destroy()
        run_gomoku_game(difficulty, first_player)

    selection_window = tk.Tk()
    selection_window.title("Select Difficulty and First Player")

    Label(selection_window, text="Select Game Difficulty", font=("Arial", 16)).pack(
        pady=10
    )

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


if __name__ == "__main__":
    select_difficulty()
