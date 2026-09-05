from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

DIFFICULTIES = {'easy': 40, 'medium': 32, 'hard': 26}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', 'medium').lower()
    if difficulty not in DIFFICULTIES:
        return jsonify({'error': 'Difficulty must be easy, medium, or hard'}), 400
    puzzle, solution = sudoku_logic.generate_puzzle(DIFFICULTIES[difficulty])
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle, 'difficulty': difficulty})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.get_json(silent=True) or {}
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    if not sudoku_logic.is_valid_board(board):
        return jsonify({'error': 'Board must be a valid 9x9 grid containing numbers from 0 to 9'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect, 'complete': not incorrect})

@app.route('/hint', methods=['POST'])
def hint():
    solution = CURRENT.get('solution')
    puzzle = CURRENT.get('puzzle')
    if solution is None or puzzle is None:
        return jsonify({'error': 'No game in progress'}), 400
    data = request.get_json(silent=True) or {}
    board = data.get('board')
    if not sudoku_logic.is_valid_board(board):
        return jsonify({'error': 'Board must be a valid 9x9 grid containing numbers from 0 to 9'}), 400
    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] == sudoku_logic.EMPTY and board[row][col] != solution[row][col]:
                return jsonify({'row': row, 'col': col, 'value': solution[row][col]})
    return jsonify({'message': 'No hint is available; the puzzle is complete.'})

if __name__ == '__main__':
    app.run()