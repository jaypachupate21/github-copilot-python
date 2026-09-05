import sudoku_logic
import pytest

from app import app


UNIQUE_PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def test_unique_and_multiple_solution_counts():
    assert sudoku_logic.count_solutions(UNIQUE_PUZZLE) == 1
    assert sudoku_logic.count_solutions(sudoku_logic.create_empty_board()) == 2


@pytest.mark.parametrize(
    'board',
    [
        [[1, 1, 0, 0, 0, 0, 0, 0, 0]] + [[0] * 9 for _ in range(8)],
        [[1, 0, 0, 0, 0, 0, 0, 0, 0], [1] + [0] * 8] + [[0] * 9 for _ in range(7)],
        [[1, 0, 0, 1, 0, 0, 0, 0, 0]] + [[0] * 9 for _ in range(8)],
        [[10] + [0] * 8] + [[0] * 9 for _ in range(8)],
        [[-1] + [0] * 8] + [[0] * 9 for _ in range(8)],
    ],
)
def test_invalid_boards_are_rejected(board):
    assert not sudoku_logic.is_valid_board(board)
    assert sudoku_logic.count_solutions(board) == 0


def test_generated_puzzles_are_valid_unique_and_have_expected_clues():
    for clues in (40, 32, 26):
        puzzle, solution = sudoku_logic.generate_puzzle(clues)
        assert len(puzzle) == sudoku_logic.SIZE
        assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
        assert sudoku_logic.is_valid_board(puzzle)
        assert sudoku_logic.count_solutions(puzzle) == 1
        assert sum(value != 0 for row in puzzle for value in row) == clues
        for row in range(sudoku_logic.SIZE):
            for col in range(sudoku_logic.SIZE):
                if puzzle[row][col] != 0:
                    assert puzzle[row][col] == solution[row][col]


def test_invalid_clue_count_is_rejected():
    with pytest.raises(ValueError):
        sudoku_logic.generate_puzzle(16)


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_home_and_difficulty_endpoints(client):
    assert client.get('/').status_code == 200
    for difficulty, clues in (('easy', 40), ('medium', 32), ('hard', 26)):
        response = client.get(f'/new?difficulty={difficulty}')
        data = response.get_json()
        assert response.status_code == 200
        assert data['difficulty'] == difficulty
        assert sum(value != 0 for row in data['puzzle'] for value in row) == clues
    assert client.get('/new?difficulty=unknown').status_code == 400


def test_check_and_hint_endpoints(client):
    puzzle_response = client.get('/new?difficulty=easy')
    puzzle = puzzle_response.get_json()['puzzle']
    check_response = client.post('/check', json={'board': puzzle})
    assert check_response.status_code == 200
    assert check_response.get_json()['complete'] is False
    hint_response = client.post('/hint', json={'board': puzzle})
    hint = hint_response.get_json()
    assert hint_response.status_code == 200
    assert puzzle[hint['row']][hint['col']] == 0
    assert 1 <= hint['value'] <= 9


def test_board_shape_is_validated_by_routes(client):
    client.get('/new?difficulty=easy')
    response = client.post('/check', json={'board': [[0]]})
    assert response.status_code == 400