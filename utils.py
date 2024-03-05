import os
from constants import SCORE_FILE


def load_game_scores():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            scores = file.read().split(",")
            return int(scores[0]), int(scores[1])
    return (
        float("inf"),
        0,
    )  # Initialize lowest round to infinity and highest score to 0


def update_game_scores(Gomoku):
    if Gomoku.move_count < Gomoku.lowest_round:
        Gomoku.lowest_round = Gomoku.move_count
    if Gomoku.human_score > Gomoku.highest_score:
        Gomoku.highest_score = Gomoku.human_score
    with open(SCORE_FILE, "w") as file:
        file.write(f"{Gomoku.lowest_round},{Gomoku.human_score}")
    Gomoku.update_scoreboard()
