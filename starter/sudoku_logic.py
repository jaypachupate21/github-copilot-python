import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def is_valid_board(board):
    if not isinstance(board, list) or len(board) != SIZE:
        return False
    for row in board:
        if not isinstance(row, list) or len(row) != SIZE:
            return False
        if any(not isinstance(value, int) or value < EMPTY or value > SIZE for value in row):
            return False
    for row in range(SIZE):
        values = [value for value in board[row] if value != EMPTY]
        if len(values) != len(set(values)):
            return False
    for col in range(SIZE):
        values = [board[row][col] for row in range(SIZE) if board[row][col] != EMPTY]
        if len(values) != len(set(values)):
            return False
    for box_row in range(0, SIZE, 3):
        for box_col in range(0, SIZE, 3):
            values = [
                board[row][col]
                for row in range(box_row, box_row + 3)
                for col in range(box_col, box_col + 3)
                if board[row][col] != EMPTY
            ]
            if len(values) != len(set(values)):
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def count_solutions(board, limit=2):
    """Count solutions, stopping as soon as the requested limit is reached."""
    if not is_valid_board(board):
        return 0

    working = deep_copy(board)
    count = 0

    def search():
        nonlocal count
        if count >= limit:
            return
        best_cell = None
        best_candidates = None
        for row in range(SIZE):
            for col in range(SIZE):
                if working[row][col] != EMPTY:
                    continue
                candidates = [
                    value for value in range(1, SIZE + 1)
                    if is_safe(working, row, col, value)
                ]
                if not candidates:
                    return
                if best_candidates is None or len(candidates) < len(best_candidates):
                    best_cell = (row, col)
                    best_candidates = candidates
        if best_cell is None:
            count += 1
            return
        row, col = best_cell
        for value in best_candidates:
            working[row][col] = value
            search()
            working[row][col] = EMPTY
            if count >= limit:
                return

    search()
    return count

def remove_cells(board, clues):
    if not isinstance(clues, int) or not 0 <= clues <= SIZE * SIZE:
        raise ValueError('clues must be between 0 and 81')
    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    current_clues = SIZE * SIZE
    for row, col in cells:
        if current_clues <= clues:
            break
        value = board[row][col]
        board[row][col] = EMPTY
        if count_solutions(board) == 1:
            current_clues -= 1
        else:
            board[row][col] = value

def generate_puzzle(clues=35):
    if not isinstance(clues, int) or not 17 <= clues <= SIZE * SIZE:
        raise ValueError('clues must be between 17 and 81')
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution
