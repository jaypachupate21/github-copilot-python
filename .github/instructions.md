# Sudoku Game — Development Instructions

## Purpose

This project is an existing Python Flask Sudoku application.

The goal is to improve the current implementation and complete the missing functionality without unnecessarily replacing working code.

### Important

**Do not rebuild the application from scratch.**

Before making changes:

1. Inspect the existing project structure.
2. Understand the current Flask routes and Sudoku logic.
3. Check the existing HTML, CSS, and JavaScript.
4. Identify which requested features are already implemented.
5. Keep existing working functionality.
6. Modify or extend the existing code only where required.

Avoid creating duplicate functions, routes, styles, or JavaScript logic when an existing implementation can be reused.

---

# Required Features

The completed application should support the following functionality.

## Sudoku Gameplay

The application must provide a standard 9×9 Sudoku board.

The player should be able to:

* Start a new puzzle.
* Enter numbers into editable cells.
* See which cells are fixed by the puzzle.
* Complete the puzzle normally.
* Receive feedback when an entry is invalid.

The Sudoku rules must be enforced for:

* Rows
* Columns
* 3×3 regions

Do not allow players to modify cells that were originally provided by the puzzle.

---

## Difficulty Levels

Provide three difficulty options:

* Easy
* Medium
* Hard

Changing the difficulty should generate a new puzzle with an appropriate number of initially filled cells.

The exact number of clues can be adjusted based on the existing implementation, but the levels should clearly differ in difficulty.

When a new difficulty is selected:

* Generate a new puzzle.
* Clear the previous board.
* Reset the timer.
* Clear old validation messages.
* Reset the solved state.

---

# Sudoku Generation

Use the existing Sudoku generation code if it is already working.

Only improve or replace it if necessary.

Every generated puzzle must have **exactly one valid solution**.

The application must not rely on random removal of numbers without checking the resulting puzzle.

A suitable approach is:

1. Create a complete valid Sudoku solution.
2. Remove values to create the playable puzzle.
3. Check how many solutions remain.
4. Keep the puzzle only if it has one solution.
5. Continue until the desired difficulty is reached.

---

# Unique Solution Check

The project needs a reliable way to determine whether a puzzle has one solution.

Implement or improve the existing solver so that it can determine whether:

* No solution exists.
* Exactly one solution exists.
* More than one solution exists.

For puzzle generation, only accept:

```python
number_of_solutions == 1
```

The solution counter should stop once it finds more than one solution. There is no need to calculate every possible solution.

This check is important because a playable Sudoku puzzle should not have multiple valid answers.

---

# Move Validation

Give the player feedback as soon as an invalid value is entered.

An entry should be considered invalid if it violates Sudoku rules.

The UI should make the problematic cell obvious without interrupting gameplay with unnecessary popup dialogs.

Possible visual feedback includes:

* Error border
* Different background
* Error indicator
* Short message near the board

Correct entries should not receive error styling.

---

# Check Button

Add or complete the **Check** functionality.

When the player presses **Check**:

1. Examine the values entered by the player.
2. Compare them with the generated solution.
3. Highlight incorrect entries.
4. Leave correct entries unchanged.
5. Do not automatically solve the board.

The player should still be able to correct the highlighted cells themselves.

---

# Hint Button

Add or complete the **Hint** functionality.

When the player requests a hint:

1. Find an editable cell that is not correctly filled.
2. Insert the correct value from the solution.
3. Mark that cell as a hint.
4. Lock the cell.
5. Give the hinted cell a visual distinction.

A hint must never insert an incorrect value.

If there are no cells available for a hint, show an appropriate message rather than changing an already completed cell.

---

# Detecting a Completed Puzzle

After player input, determine whether the puzzle has been solved.

A puzzle is complete only when:

* Every cell contains a number.
* The board satisfies Sudoku rules.
* The player's values match the actual solution.

Once the puzzle is solved:

* Stop the timer.
* Display a success message.
* Show the completion time.
* Ask for the player's name.
* Save the result to the leaderboard.

Do not record unfinished games.

---

# Timer

The game should include a timer showing how long the player has been solving the current puzzle.

Expected behavior:

* Start when a new puzzle begins.
* Continue while the puzzle is being played.
* Stop when the puzzle is solved.
* Reset when a new puzzle starts.
* Reset when difficulty changes.

Store the elapsed time as seconds for leaderboard sorting.

Display it in a readable format such as:

```text
00:00
01:25
12:48
01:02:15
```

The timer should be handled on the client side rather than relying on a Flask request for every second.

---

# Top 10 Leaderboard

Create a Top 10 leaderboard using browser `localStorage`.

Each result should contain at least:

```javascript
{
    name: "Player",
    time: 125,
    difficulty: "Medium"
}
```

Use a consistent localStorage key, for example:

```text
sudokuLeaderboard
```

The leaderboard should:

* Keep the best 10 results.
* Sort results by completion time.
* Show player name.
* Show time.
* Show difficulty.
* Remain available after refreshing the page.

If localStorage contains invalid or corrupted data, the application should recover gracefully instead of crashing.

Player names should be inserted into the page safely. Do not inject raw user input using `innerHTML`.

---

# Dark Mode

The application should have a Dark Mode toggle.

Changing the theme should affect the complete application rather than only the Sudoku board.

The following should adapt to the selected theme:

* Page background
* Cards/panels
* Sudoku cells
* Borders
* Text
* Buttons
* Inputs
* Difficulty selector
* Timer
* Leaderboard
* Messages
* Error states
* Hint states

Prefer CSS variables so the theme can be maintained from a central location.

For example:

```css
:root {
    --background: #ffffff;
    --text: #222222;
}

[data-theme="dark"] {
    --background: #121212;
    --text: #ffffff;
}
```

The selected theme should preferably be remembered with localStorage.

---

# Sudoku Box Appearance

Make the nine 3×3 Sudoku regions visually recognizable.

Use alternating backgrounds or subtle differences between neighboring regions.

The styling must remain readable in both themes.

Error and hint states must still be visible when placed over the box backgrounds.

Do not use colors that make the Sudoku numbers difficult to read.

---

# Responsive Layout

The existing UI should work on both desktop and mobile screens.

The Sudoku board should remain square and scale according to the available screen width.

Pay particular attention to:

* Cell size
* Button size
* Difficulty selector
* Timer
* Leaderboard
* Spacing
* Text size
* Dark mode controls

Avoid fixed desktop-only widths.

The page should not require horizontal scrolling on normal mobile screen sizes.

Test approximately at:

```text
320px
375px
768px
1024px
1440px
```

---

# UI Consistency

Keep the existing visual design where it is already good.

When modifying the interface:

* Maintain consistent fonts.
* Use consistent spacing.
* Keep button styles consistent.
* Maintain readable text.
* Provide visible hover/focus states.
* Avoid unnecessary animations.
* Keep controls easy to understand.

Do not introduce a completely different design unless the current UI requires it.

---

# Flask Integration

Reuse the existing Flask application and routes whenever possible.

If a new endpoint is required, follow the existing project's naming and response conventions.

A new-game request should be able to identify the requested difficulty.

For example:

```text
/api/new-game?difficulty=easy
```

The exact route may differ if the existing project already has an equivalent endpoint.

Do not create a second route that performs the same operation.

Validate difficulty values on the server.

Valid values:

```text
easy
medium
hard
```

---

# Code Organization

Follow the structure already present in the project.

If the existing code is reasonably organized, extend it rather than moving everything around.

If Sudoku logic is currently mixed into Flask routes and separating it can be done safely, consider organizing it into logical modules such as:

```text
generator.py
solver.py
validator.py
```

However, **do not perform large-scale restructuring simply for the sake of matching this document.**

The priority is to improve the existing application safely.

---

# Testing

Testing is required before considering the implementation complete.

Use the existing test framework if one is already present.

If no testing framework exists, use `pytest` for Python tests.

---

## Sudoku Solver Tests

Test the solver with:

### Valid Puzzle

Confirm that a known valid puzzle can be solved.

### Correct Solution

Verify that the returned solution satisfies:

* All rows contain 1–9.
* All columns contain 1–9.
* All 3×3 regions contain 1–9.

### Unsolvable Puzzle

Give the solver an invalid puzzle and confirm that it identifies that no solution exists.

### Unique Solution

Verify that a known uniquely solvable puzzle returns:

```python
count_solutions(puzzle) == 1
```

### Multiple Solutions

Verify that a puzzle with multiple possible solutions is detected correctly.

---

# Puzzle Generator Tests

Generate several puzzles for:

* Easy
* Medium
* Hard

For each generated puzzle verify:

* The board is 9×9.
* The puzzle is valid.
* A solution exists.
* The solution is unique.
* Existing clues agree with the solution.
* Difficulty levels produce different numbers of clues.

Do not test only one randomly generated puzzle. Run multiple generations because the generator is randomized.

---

# Validator Tests

Test cases should include:

* Valid number.
* Duplicate number in a row.
* Duplicate number in a column.
* Duplicate number in a 3×3 region.
* Invalid number below 1.
* Invalid number above 9.
* Empty cell.
* Invalid coordinates where applicable.

---

# Flask Tests

Test the existing Flask endpoints.

At minimum verify:

* Home page loads successfully.
* New puzzle can be requested.
* Easy puzzle can be generated.
* Medium puzzle can be generated.
* Hard puzzle can be generated.
* Invalid difficulty is rejected appropriately.
* Returned puzzle has the expected structure.

Do not test only HTTP status codes. Where practical, validate the returned JSON data as well.

---

# Frontend Manual Testing

Before completing the task, manually test the complete user flow.

### New Game

* Open the application.
* Generate a puzzle.
* Confirm the board appears correctly.
* Confirm fixed cells cannot be edited.
* Confirm editable cells accept input.
* Confirm the timer starts.

### Difficulty

Test all three levels.

Confirm that changing difficulty creates a new puzzle and resets the game state.

### Invalid Input

Enter an invalid value and confirm that the corresponding cell receives feedback.

### Check

Enter an incorrect value and press Check.

Confirm that the incorrect value is highlighted.

### Hint

Press Hint.

Confirm that:

* One correct value appears.
* The cell becomes locked.
* The cell is visually recognizable as a hint.

### Solve

Complete a puzzle.

Confirm:

* Success message appears.
* Timer stops.
* Time is displayed.
* Player name can be entered.
* Result is saved.

### Leaderboard

Create several results and confirm:

* Results persist after refresh.
* Results are sorted correctly.
* Only the best 10 are retained.
* Difficulty is displayed.

### Dark Mode

Toggle the theme.

Confirm that the complete page changes appearance.

Refresh the page and verify that the selected theme remains active.

### Mobile

Test the game on a narrow viewport and make sure the board and controls remain usable.

---

# Regression Testing

Because this is an existing project, every change must be checked against existing functionality.

After implementing a feature:

1. Run the automated tests.
2. Start the Flask application.
3. Test the affected feature manually.
4. Test the basic game flow again.

Do not fix one feature by breaking another.

---

# Copilot Working Rules

When working on this project, follow these rules strictly:

1. **Inspect existing code before writing new code.**
2. Reuse existing functions whenever possible.
3. Do not duplicate existing functionality.
4. Do not replace working Sudoku logic without a reason.
5. Do not replace the existing UI unnecessarily.
6. Make the smallest practical changes to achieve the requested features.
7. Keep Sudoku generation, solving, validation, and UI concerns reasonably separated.
8. Do not bypass the unique-solution requirement.
9. Do not hardcode a single puzzle.
10. Do not use a database for the leaderboard unless the project requirements are changed later.
11. Use localStorage for leaderboard and theme persistence.
12. Keep user input safe when rendering it.
13. Maintain responsive behavior.
14. Ensure light and dark modes remain readable.
15. Add or update tests when changing Sudoku logic.
16. Run the tests after significant changes.
17. Fix regressions before moving on.
18. Avoid unnecessary dependencies.
19. Do not expose server-side stack traces to users.
20. Do not mark the task complete until the complete game flow has been tested.

---

# Completion Checklist

Before finishing, verify the following:

* [ ] Existing code was inspected before modification.
* [ ] Sudoku board works.
* [ ] Easy difficulty works.
* [ ] Medium difficulty works.
* [ ] Hard difficulty works.
* [ ] Difficulty changes puzzle generation.
* [ ] Every generated puzzle has exactly one solution.
* [ ] Fixed cells cannot be changed.
* [ ] Player input is validated.
* [ ] Invalid moves receive immediate feedback.
* [ ] Check button highlights incorrect entries.
* [ ] Hint button fills a correct cell.
* [ ] Hint cells become locked.
* [ ] Puzzle completion is detected correctly.
* [ ] Completion message is displayed.
* [ ] Timer starts and stops correctly.
* [ ] Top 10 leaderboard works.
* [ ] Leaderboard uses localStorage.
* [ ] Leaderboard survives page refresh.
* [ ] Only the best 10 scores are retained.
* [ ] Difficulty is stored with each score.
* [ ] Dark mode works across the entire UI.
* [ ] Dark mode preference persists.
* [ ] 3×3 boxes have alternating visual styling.
* [ ] Desktop layout works.
* [ ] Mobile layout works.
* [ ] Text and controls remain readable.
* [ ] Automated tests pass.
* [ ] Manual testing passes.
* [ ] Existing functionality has not been broken.

---

# Final Instruction to Copilot

**Work with the existing project, not against it.**

First understand what is already implemented. Then identify missing or incomplete requirements from this document and implement them one at a time.

Prefer small, focused changes over a complete rewrite.

After implementation, run the tests and manually verify the main Sudoku gameplay flow before considering the work finished.
