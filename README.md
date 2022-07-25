# Python Puzzle Game Board Project

This program (puzzle.py) is for solving both word puzzles and math puzzles on a 2D game board. 


The superclass Puzzle is an abstract base class (ABC) which defines an abstract method called solve(). Two concrete subclasses named WordPuzzle and MathPuzzle are derived from Puzzle. They override the parent solve() method with their own versions for solving the puzzle with different logics – one is to locate all correct English words on the game board while another is to find the maximum product of a fixed-size list of adjacent numbers on the board.
