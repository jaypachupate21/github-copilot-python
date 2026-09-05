# Sudoku Game

A Flask-powered Sudoku game with uniquely solvable puzzles, difficulty levels, hints, immediate move validation, a client-side timer, dark mode, and a persistent local leaderboard.

Repository: <https://github.com/jaypachupate21/github-copilot-python>

## Features

- 9x9 Sudoku board with fixed clues and editable cells.
- Easy, Medium, and Hard puzzles with 40, 32, and 26 clues respectively.
- Puzzle generation that checks for exactly one valid solution.
- Immediate row, column, and 3x3 region conflict feedback.
- Check action that highlights entries that do not match the generated solution.
- Hint action that fills and locks one correct editable cell.
- Completion detection with elapsed time and optional player name.
- Top 10 leaderboard stored in browser `localStorage`.
- Persistent light/dark theme preference.
- Responsive layout for desktop and mobile screens.

## Requirements

- Python 3.10 or newer recommended.
- A modern web browser.

## Setup

From the repository root, create and activate a virtual environment:

```bash
cd github-copilot-python/starter
python -m venv .venv
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Open <http://127.0.0.1:5000> in a browser.

## Testing

Run the automated test suite from the `starter` directory:

```bash
python -m pytest -q
```

The tests cover solution counting, invalid boards, puzzle generation, difficulty levels, Flask routes, hints, and malformed requests.

## API Routes

### `GET /`

Serves the game interface.

### `GET /new?difficulty=<level>`

Starts a new game. Valid difficulty values are `easy`, `medium`, and `hard`.

Example response:

```json
{
	"difficulty": "medium",
	"puzzle": [[0, 4, 0,  ...]]
}
```

### `POST /check`

Checks a board against the current solution.

Request body:

```json
{
	"board": [[0, 4, 0, ...]]
}
```

The response contains the incorrect cell coordinates and a `complete` flag.

### `POST /hint`

Returns one correct value for an editable cell. The browser inserts the value and locks the cell as a hint. When no hint is available, the route returns a message instead.

## Data and Privacy

The current puzzle and solution are kept in server memory for the active Flask process. Leaderboard scores and the selected theme are stored only in the browser's `localStorage`; no user accounts or database are used.

## Project Structure

```text
starter/
	app.py                 Flask routes and application entry point
	sudoku_logic.py        Board validation, solving, and puzzle generation
	requirements.txt       Python dependencies
	static/
		main.js              Browser interaction, timer, theme, and leaderboard
		styles.css            Responsive light/dark styling
	templates/
		index.html            Game page
	tests/
		test_sudoku.py       Automated backend and generator tests
```
