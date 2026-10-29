# Taskboard

Taskboard is a simple local CLI task-list manager with SQLite persistence. It supports adding, listing, and completing tasks, with robust validation and JSON output. No third-party dependencies are required.

## Usage

Run commands using:

    python -m taskboard --database PATH <subcommand> [args]

- `--database PATH` (optional): Path to the SQLite database file (default: `tasks.sqlite3` in the current directory).
- Subcommands:
    - `add TITLE`: Add a new task with the given title.
    - `list`: List all tasks.
    - `complete ID`: Mark the task with the given ID as completed.

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

## Running Tests

To run the unittests:

    python -m unittest discover tests

This will execute all tests in the `tests/` directory, covering validation, state transitions, and persistence.
