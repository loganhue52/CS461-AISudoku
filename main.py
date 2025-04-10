from PyQt6.QtWidgets import QApplication
import sys
from ui import SudokuGUI  # Import the GUI class

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuGUI()
    window.show()
    sys.exit(app.exec())
