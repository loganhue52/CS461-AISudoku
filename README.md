# AI Sudoku Solver

A simple, animated Sudoku solver built with PyQt6. This project generates random Sudoku puzzles and solves them visually using a step-by-step backtracking algorithm.

## Features

- Random puzzle generation with difficulty levels: Easy, Medium, Hard
- AI backtracking solver with real-time visualization
- PyQt GUI with bold 3x3 grid lines
- Pre-filled numbers are shown in blue and are not editable
- Solve and Reset buttons for user interaction

## Installation

1. Clone the repository: https://github.com/loganhue52/CS461-AISudoku.git
2. Install dependencies: pip install PyQt6
3. Run the application: python main.py

## File Structure
CS461-AISudoku/ 

├── main.py # Entry point 

├── ui.py # PyQt GUI 

├── solver.py # AI solving logic (backtracking + animation) 

├── generator.py # Random puzzle generator 

└── README.md # Project documentation

## How It Works

- The solver uses a backtracking algorithm to find a valid solution.
- A generator yields each step in the solving process, which is animated in the GUI.
- Difficulty level controls the number of pre-filled cells.
- The grid is updated in real time as the solver attempts and backtracks on values.


## License

This project was developed for CS461 - Final Project. All rights reserved.
