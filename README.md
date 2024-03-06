# Gomoku Game Guide

Welcome to the Gomoku Game! Gomoku, also known as Five in a Row, is a strategy board game that is traditionally played with Go pieces (black and white stones) on a Go board. This digital version brings the classic game to your computer, offering multiple AI difficulty levels to challenge players of all ages and skill levels. Let me tell you a secret, Gomoku was actually my favorite chess game when I was in elementary school!
<br/><hr/><p>This game is developed by <a href="https://honeymeat.github.io/">Jamie Nagy</a>.</p><hr/>

## Game Update
Version 1.0 released!
Just to let you know I'm working on future updates!

## How to Play

Follow these steps to get started with the Gomoku game:

### 1. Clone the Repository or Download the Files

To get the game, clone the repository using Git or download all the files into one directory.

If you're familiar with Git, you can clone the repository with the following command:

```bash
git clone https://github.com/HoneyMeat/Jamie-Gomoku.git
```

### 2. Check Python Version

Ensure you have Python installed on your system. This game is tested with Python 3.12.1, but it should be compatible with recent Python 3.x versions. To check your Python version, run:

```bash
python --version
```

### 3. Set Up a Virtual Environment

It's recommended to run the game in a virtual environment. Navigate to the game directory and create a virtual environment:

```bash
cd path/to/gomoku
python -m venv venv
```

Activate the virtual environment:

On Windows:

```bash
.\venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

### 4. Run the Game

With the virtual environment activated, launch the game by running:

```bash
python app.py
```

## Game Levels

The game offers three AI difficulty levels:

- **Easy Level**: Ideal for toddlers or players who don't know the rule yet, providing a gentle introduction to the game.
- **Medium Level**: Designed for beginners, offering a moderate challenge.
- **Hard Level**: The ultimate challenge! I strongly recommend you to have a go with this level. Even I got beat by my own AI many times🤣  Please note that the AI may take 10-20 seconds to think as the game progresses. Your patience is appreciated!

## Score Tracking

Your highest scores and the lowest number of rounds used to win are recorded in `game_scores.txt`. This allows you to track your progress and achievements over time.

Enjoy the game, and may the best strategist win!
