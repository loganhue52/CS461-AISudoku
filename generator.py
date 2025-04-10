from solver import solve_sudoku, is_valid
import random

def generate_sudoku(difficulty="medium"):
    board = [[0] * 9 for _ in range(9)]
    fill_board(board)
    if difficulty == "easy":
        num_remove = 35
    elif difficulty == "medium":
        num_remove = 45
    else:
        num_remove = 55

    for _ in range(num_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

    return board

def fill_board(board):
    nums = list(range(1, 10))

    def helper():
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    random.shuffle(nums)
                    for num in nums:
                        if is_valid(board, num, row, col):
                            board[row][col] = num
                            if helper():
                                return True
                            board[row][col] = 0
                    return False
        return True

    helper()
