# Copyright 2025 Andrés Montes Zuluaga
# Licensed under the Apache License, Version 2.0 (see LICENSE file)

"""
TicTacToe - Main Entry Point

This file acts as the central bootstrapper for the TicTacToe game,
instantiating the game logic (Board), the computer player AI (AI), and the GUI described in gui.py.

- All user interaction is handled by the GameGUI class.
- The Board class encapsulates all game state, rule enforcement, and victory/draw checking.
- The AI class can be configured to different difficulty levels, as selected by the user in the GUI.

The entire game should always be run and tested from this main.py file.

"""

from src.logic import Board
from src.ai import get_ai_player
from src.gui import GameGUI

def main():
    """
    Sets up the game environment and launches the GUI.
    By default, starts with no AI ("human vs human"), but GameGUI is designed to switch to computer opponent
    when requested by the player.
    """
    board = Board(size=3)
    # We do not know yet which AI level, but GUI will manage the player selection,
    # so we create a dummy AI for now. GameGUI should be able to instantiate the right level as needed.
    # The mark is "O" by convention for computer.
    ai = get_ai_player(level="easy", mark="O", max_time=1.0)
    gui = GameGUI(board, ai)
    gui.run()

if __name__ == "__main__":
    main()