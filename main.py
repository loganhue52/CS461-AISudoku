import tkinter as tk
from tkinter import messagebox
import random
import copy

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        
        self.puzzle, self.solution = self.generate_puzzle(removals=40)
        self.board = copy.deepcopy(self.puzzle)
        self.fixed = [[(cell != 0) for cell in row] for row in self.board]
        
        self.create_grid()
        self.create_buttons()
    
    def create_grid(self):
        self.cells = []
        for i in range(9):
            row_cells = []
            for j in range(9):
                frame = tk.Frame(self.root, width=50, height=50, highlightbackground="black", highlightthickness=1)
                if i % 3 == 0 and i != 0:
                    frame.config(highlightthickness=2)
                if j % 3 == 0 and j != 0:
                    frame.config(highlightthickness=2)
                frame.grid(row=i, column=j, padx=(2 if j % 3 == 0 else 0), pady=(2 if i % 3 == 0 else 0))
                
                entry = tk.Entry(frame, width=2, font=("Arial", 18), justify="center")
                entry.grid(sticky="nsew")
                
                if self.puzzle[i][j] != 0:
                    entry.insert(0, str(self.puzzle[i][j]))
                    entry.config(state="disabled", disabledforeground="black")
                else:
                    entry.bind("<KeyRelease>", lambda event, x=i, y=j: self.validate_entry(event, x, y))
                
                row_cells.append(entry)
            self.cells.append(row_cells)
    
    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=9, column=0, columnspan=9, pady=10)
        
        solve_btn = tk.Button(button_frame, text="Solve", command=self.solve)
        solve_btn.pack(side="left", padx=10)
        
        reset_btn = tk.Button(button_frame, text="Reset", command=self.reset)
        reset_btn.pack(side="left", padx=10)
    
    def validate_entry(self, event, row, col):
        value = self.cells[row][col].get()
        if not (value.isdigit() and 1 <= int(value) <= 9):
            self.cells[row][col].delete(0, tk.END)
    
    def solve(self):
        for i in range(9):
            for j in range(9):
                if not self.fixed[i][j]:
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(self.solution[i][j]))
    
    def reset(self):
        for i in range(9):
            for j in range(9):
                if not self.fixed[i][j]:
                    self.cells[i][j].delete(0, tk.END)
    
    def generate_full_board(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_board(board)
        return board
    
    def generate_puzzle(self, removals=40):
        full_board = self.generate_full_board()
        puzzle = copy.deepcopy(full_board)
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        removed = 0
        for row, col in cells:
            if removed >= removals:
                break
            temp = puzzle[row][col]
            puzzle[row][col] = 0
            if self.count_solutions(puzzle) != 1:
                puzzle[row][col] = temp
            else:
                removed += 1
        
        return puzzle, full_board
    
    def solve_board(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self.is_valid_move(board, i, j, num):
                            board[i][j] = num
                            if self.solve_board(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    
    def is_valid_move(self, board, row, col, num):
        if any(board[row][j] == num for j in range(9)) or any(board[i][col] == num for i in range(9)):
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True
    
    def count_solutions(self, board, limit=2):
        count = 0
        def backtrack(bd):
            nonlocal count
            if count >= limit:
                return
            for i in range(9):
                for j in range(9):
                    if bd[i][j] == 0:
                        for num in range(1, 10):
                            if self.is_valid_move(bd, i, j, num):
                                bd[i][j] = num
                                backtrack(bd)
                                bd[i][j] = 0
                        return
            count += 1
        board_copy = copy.deepcopy(board)
        backtrack(board_copy)
        return count

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()