# Sudoku Game

A Flask Sudoku game with generated puzzles, unique-solution validation, difficulty levels, hints, a timer, a local leaderboard, and light/dark themes.

## Features

- 9x9 Sudoku board with locked puzzle clues.
- Easy, Medium, and Hard puzzles with 40, 32, and 26 clues respectively.
- Puzzle generation that accepts only puzzles with exactly one solution.
- Row, column, and 3x3 region validation.
- Immediate visual feedback for conflicting entries.
- Check button for comparing entries with the generated solution.
- Hint button that inserts and locks a correct value.
- Leaderboard entries include the number of hints used.
- Client-side timer that stops when the puzzle is solved.
- Top 10 leaderboard stored in browser `localStorage` under `sudokuLeaderboard`.
- Persistent light/dark theme preference stored under `sudokuTheme`.
- Responsive layout for desktop and mobile screens.

## Requirements

- Python 3.10 or newer
- A modern web browser

## Setup

From the repository root, create and activate a virtual environment, then install the dependencies.

### Windows PowerShell

```powershell
cd starter
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS or Linux

```bash
cd starter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the application

From the `starter` directory:

```bash
python app.py
```

Open <http://127.0.0.1:5000> in a browser.

## Run tests

From the `starter` directory:

```bash
python -m pytest -q
```

The test suite covers solution counting, invalid boards, generated puzzle uniqueness, clue counts, difficulty routes, checking, hints, and malformed requests.

## Project structure

```text
starter/
	app.py                 Flask application and API routes
	sudoku_logic.py        Board validation, solving, and puzzle generation
	requirements.txt       Python dependencies
	tests/test_sudoku.py   Automated tests
	templates/index.html   Game markup
	static/main.js         Board interaction and client-side game state
	static/styles.css      Responsive light/dark styling
```

## API endpoints

### `GET /`

Serves the game page.

### `GET /new?difficulty=<level>`

Creates a new puzzle. Valid difficulty values are `easy`, `medium`, and `hard`.

Example response:

```json
{
	"difficulty": "medium",
	"puzzle": [[0, 0, 5,  ...]]
}
```

### `POST /check`

Compares a submitted board with the current puzzle solution.

Request body:

```json
{
	"board": [[0, 0, 5,  ...]]
}
```

The response includes `incorrect`, an array of incorrect `[row, column]` positions, and `complete`.

### `POST /hint`

Accepts the current board and returns one correct editable cell:

```json
{
	"row": 0,
	"col": 1,
	"value": 7
}
```

The browser locks the returned cell after applying the hint. When no hint is available, the endpoint returns a message instead.

## Notes

- The current puzzle and solution are held in Flask memory, so restarting the server starts a new game state.
- Leaderboard entries and theme preference are browser-local and are not shared between browsers or devices.
- Player names are rendered with DOM text nodes rather than raw HTML.
