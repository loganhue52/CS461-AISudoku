from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QComboBox
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt, QTimer
import sys
import generator
import solver

class SudokuGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setGeometry(100, 100, 500, 550)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.create_grid()
        self.create_controls()

        self.solving = False
        self.timer = None
        self.solve_stack = []
        self.step_generator = None

        self.new_puzzle()

    def create_grid(self):
        """Creates a 9x9 Sudoku board with proper formatting."""
        self.cells = []
        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = QLineEdit(self)
                cell.setMaxLength(1)
                cell.setFixedSize(50, 50)
                cell.setFont(QFont("Arial", 20))
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Add bold borders for subgrids
                top = 2 if row % 3 == 0 else 1
                left = 2 if col % 3 == 0 else 1
                bottom = 2 if row == 8 else 1
                right = 2 if col == 8 else 1
                cell.setStyleSheet(f"border-top: {top}px solid black; "
                                   f"border-left: {left}px solid black; "
                                   f"border-bottom: {bottom}px solid black; "
                                   f"border-right: {right}px solid black; ")

                self.grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def solve_step(self):
        try:
            action, row, col, value = next(self.step_generator)

            if action == "place":
                self.board[row][col] = value
                self.cells[row][col].setText(str(value))
                self.cells[row][col].setStyleSheet(self.cells[row][col].styleSheet() + "color: black; background-color: white;")
            elif action == "remove":
                self.board[row][col] = 0
                self.cells[row][col].clear()
                self.cells[row][col].setStyleSheet(self.cells[row][col].styleSheet() + "background-color: #fdd;")  # light red on backtrack
            elif action == "done":
                self.timer.stop()
        except StopIteration:
            self.timer.stop()

    def create_controls(self):
        """Adds Solve, Reset buttons and Difficulty Selector."""
        self.difficulty = QComboBox()
        self.difficulty.addItems(["Easy", "Medium", "Hard"])
        self.layout.addWidget(self.difficulty)

        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_puzzle)
        self.layout.addWidget(self.solve_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.new_puzzle)
        self.layout.addWidget(self.reset_button)

    def new_puzzle(self):
        """Generates a new puzzle based on difficulty."""
        level = self.difficulty.currentText().lower()
        self.board = generator.generate_sudoku(level)
        
        for row in range(9):
            for col in range(9):
                num = self.board[row][col]
                cell = self.cells[row][col]
                if num != 0:
                    cell.setText(str(num))
                    cell.setReadOnly(True)
                    cell.setStyleSheet(cell.styleSheet() + "color: turquoise;" + "background-color: #181818;")  # Prefilled numbers in blue
                else:
                    cell.clear()
                    cell.setReadOnly(False)
                    cell.setStyleSheet(cell.styleSheet() + "color: black;"+ "background-color: #181818;")

    def solve_puzzle(self):
        """Begins animated solving process using a generator."""
        self.step_generator = solver.animated_solver(self.board)
        self.timer = QTimer()
        self.timer.timeout.connect(self.solve_step)
        self.timer.start(30)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuGUI()
    window.show()
    sys.exit(app.exec())
