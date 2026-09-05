const SIZE = 9;
const LEADERBOARD_KEY = 'sudokuLeaderboard';
const THEME_KEY = 'sudokuTheme';
let puzzle = [];
let difficulty = 'medium';
let startedAt = 0;
let timerId = null;
let solved = false;

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '').slice(0, 1);
        e.target.value = val;
        e.target.classList.remove('incorrect', 'conflict');
        validateEntry(input);
        checkComplete();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

function boardValues() {
  return Array.from({length: SIZE}, (_, row) => Array.from({length: SIZE}, (_, col) => {
    const input = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    return input.value ? Number(input.value) : 0;
  }));
}

function validateEntry(input) {
  if (!input.value) return;
  const board = boardValues();
  const row = Number(input.dataset.row);
  const col = Number(input.dataset.col);
  board[row][col] = 0;
  const conflict = board[row].includes(Number(input.value)) || board.some(values => values[col] === Number(input.value));
  const boxRow = Math.floor(row / 3) * 3;
  const boxCol = Math.floor(col / 3) * 3;
  const boxValues = board.slice(boxRow, boxRow + 3).flatMap(values => values.slice(boxCol, boxCol + 3));
  if (conflict || boxValues.includes(Number(input.value))) input.classList.add('conflict');
}

function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remaining = seconds % 60;
  return [hours, minutes, remaining].map((value, index) => index === 0 && hours === 0 ? null : String(value).padStart(2, '0')).filter(Boolean).join(':') || '00:00';
}

function updateTimer() {
  document.getElementById('timer').textContent = formatTime(Math.floor((Date.now() - startedAt) / 1000));
}

function startTimer() {
  clearInterval(timerId);
  startedAt = Date.now();
  updateTimer();
  timerId = setInterval(updateTimer, 1000);
}

function stopTimer() {
  clearInterval(timerId);
  timerId = null;
}

function setMessage(text, type = '') {
  const message = document.getElementById('message');
  message.textContent = text;
  message.className = type;
}

async function newGame() {
  difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${difficulty}`);
  const data = await res.json();
  if (!res.ok) return setMessage(data.error, 'error');
  solved = false;
  renderPuzzle(data.puzzle);
  setMessage('');
  startTimer();
}

async function checkSolution() {
  const inputs = document.querySelectorAll('.sudoku-cell');
  const board = boardValues();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  if (data.error) {
    setMessage(data.error, 'error');
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.remove('incorrect');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (incorrect.size === 0) {
    completeGame();
  } else {
    setMessage('Some cells are incorrect.', 'error');
  }
}

async function requestHint() {
  const res = await fetch('/hint', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({board: boardValues()})});
  const data = await res.json();
  if (data.error) return setMessage(data.error, 'error');
  if (data.message) return setMessage(data.message);
  const input = document.querySelector(`[data-row="${data.row}"][data-col="${data.col}"]`);
  input.value = data.value;
  input.disabled = true;
  input.classList.add('hint');
  setMessage('A correct cell was revealed.');
  checkComplete();
}

function checkComplete() {
  if (solved || boardValues().some(row => row.includes(0))) return;
  checkSolution();
}

function completeGame() {
  solved = true;
  stopTimer();
  const seconds = Math.floor((Date.now() - startedAt) / 1000);
  setMessage(`Solved in ${formatTime(seconds)}. Enter your name to save your score.`, 'success');
  const name = window.prompt('Your name:');
  if (name && name.trim()) saveScore(name.trim(), seconds);
}

function loadScores() {
  try {
    const scores = JSON.parse(localStorage.getItem(LEADERBOARD_KEY) || '[]');
    return Array.isArray(scores) ? scores.filter(score => score && typeof score.name === 'string' && Number.isFinite(score.time)) : [];
  } catch (error) { return []; }
}

function saveScore(name, time) {
  const scores = [...loadScores(), {name, time, difficulty}].sort((a, b) => a.time - b.time).slice(0, 10);
  localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(scores));
  renderLeaderboard();
}

function renderLeaderboard() {
  const list = document.getElementById('leaderboard');
  list.replaceChildren();
  loadScores().forEach(score => {
    const item = document.createElement('li');
    item.textContent = `${score.name} - ${formatTime(score.time)} (${score.difficulty})`;
    list.appendChild(item);
  });
}

function toggleTheme() {
  const dark = document.documentElement.dataset.theme !== 'dark';
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  localStorage.setItem(THEME_KEY, document.documentElement.dataset.theme);
  document.getElementById('theme-toggle').textContent = dark ? 'Light mode' : 'Dark mode';
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint').addEventListener('click', requestHint);
  document.getElementById('difficulty').addEventListener('change', newGame);
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  document.documentElement.dataset.theme = localStorage.getItem(THEME_KEY) || 'light';
  document.getElementById('theme-toggle').textContent = document.documentElement.dataset.theme === 'dark' ? 'Light mode' : 'Dark mode';
  renderLeaderboard();
  // initialize
  newGame();
});