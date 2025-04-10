def is_valid(board, num, row, col):
    """Checks if a number is valid in the given row, column, and 3x3 grid."""
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    box_x, box_y = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_x + i][box_y + j] == num:
                return False
    return True

def solve_sudoku(board):
    empty = find_empty_cell(board)
    if not empty:
        return True

    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty_cell(board):
    """Finds an empty cell (0) in the board."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def animated_solver(board):
    """Generator that yields each solving step: (action, row, col, value)"""
    def is_valid(board, num, row, col):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        box_x, box_y = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[box_x + i][box_y + j] == num:
                    return False
        return True

    def solve():
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, num, row, col):
                            board[row][col] = num
                            yield ("place", row, col, num)
                            yield from solve()
                            if all(0 not in row for row in board):
                                yield ("done", -1, -1, -1)
                                return
                            board[row][col] = 0
                            yield ("remove", row, col, 0)
                    return
        yield ("done", -1, -1, -1)

    yield from solve()