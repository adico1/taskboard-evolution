# Taskboard

Taskboard is a simple local CLI task-list manager with SQLite persistence. It supports adding, listing, completing, and renaming tasks, with robust validation and JSON output. No third-party dependencies are required.

## Usage

Run commands using:

    python -m taskboard --database PATH <subcommand> [args]

- `--database PATH` (optional): Path to the SQLite database file (default: `tasks.sqlite3` in the current directory).
- Subcommands:
    - `add TITLE`: Add a new task with the given title.
    - `list`: List all tasks.
    - `complete ID`: Mark the task with the given ID as completed.
    - `rename ID TITLE`: Rename the task with the given ID to TITLE. TITLE is trimmed of leading/trailing Unicode whitespace; internal spacing, case, and Unicode are preserved. Works for open and completed tasks. Only the title changes; ID and completion state are preserved. Success prints a JSON object with the updated task. Errors print a JSON error object to stderr and exit 2. IDs must be positive integers within SQLite's signed 64-bit range. Blank/whitespace-only titles and invalid IDs are rejected with no data change.

All successful commands print exactly one JSON value to stdout and exit 0. Errors print a JSON error object to stderr and exit 2.

## Examples

```json taskboard-examples
[
  {"args": ["add", "buy milk"], "stdout": {"id": 1, "title": "buy milk", "completed": false}},
  {"args": ["list"], "stdout": [{"id": 1, "title": "buy milk", "completed": false}]},
  {"args": ["complete", "1"], "stdout": {"id": 1, "title": "buy milk", "completed": true}}
]
```

All examples assume a fresh database. Each command is run as a new process.

```json taskboard-rename-examples
[
  {"args": ["add", "first"], "stdout": {"id": 1, "title": "first", "completed": false}},
  {"args": ["complete", "1"], "stdout": {"id": 1, "title": "first", "completed": true}},
  {"args": ["rename", "1", "renamed task"], "stdout": {"id": 1, "title": "renamed task", "completed": true}},
  {"args": ["list"], "stdout": [{"id": 1, "title": "renamed task", "completed": true}]}
]
```

## Running Tests

To run the unittests:

    python -m unittest discover tests

This will execute all tests in the `tests/` directory, covering validation, state transitions, persistence, and the rename feature.
