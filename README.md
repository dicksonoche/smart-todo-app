# DataEpic Intermediate - Smart Todo App

Simple, test-backed CLI to manage tasks with tags, priority, due dates, assignees, and time parsing.

## Features
- Add, update, delete, list tasks
- Mark complete/incomplete
- Smart parsing with regex: tags (@tag), priority (#high/#medium/#low), due (YYYY-MM-DD/tomorrow/next week), assigned email, time (at/by H:MM am/pm)
- Regex search and filtering (by description, tags, due date)
- JSON persistence

## Installation

1. Ensure Python >= 3.14 is available.
2. Use the provided virtualenv `todoENV` or install with your own tool.
3. Install deps using `poetry` or `pip`:

```bash
pip install -r <(python - <<'PY'
import tomllib, sys
data = tomllib.load(open('pyproject.toml','rb'))
for dep in data['project']['dependencies']:
    print(dep)
PY
)
```

Or with Poetry:

```bash
poetry install --no-root
```

## Running

```bash
PYTHONPATH=src python -m src.main --help
```

Interactive mode (REPL):

```bash
poetry run python -m src.main --interactive
# or simply run without a subcommand
poetry run python -m src.main
```

Within the REPL, type commands like:
- add "Buy milk @home #high"
- list --priority high
- search "milk"
- complete 1
- exit

Commands:
- `add "Buy milk @home #high due:2025-10-20 assigned:alice@example.com"`
- `delete 3`
- `update 2 "Call mom tomorrow at 3pm @family"`
- `list [--priority high] [--tag '^home$'] [--due '2025-10']`
- `complete 1` / `incomplete 1`
- `search 'grocer|milk'`

All commands accept `--data PATH` to choose an alternate storage file (defaults to `data/tasks.json`).

## Parsing Rules

- **Tags**: `@tag` (alnum and underscore)
- **Priority**: `#high`, `#medium`, `#low` (case-insensitive)
- **Due**: `due:YYYY-MM-DD`, `due:tomorrow`, `due:next week`; natural tokens without `due:` are also recognized
- **Assigned**: `assigned:email@example.com`
- **Time**: "at/by H(:MM) AM/PM"

## Development

- Run tests: `PYTHONPATH=src pytest -q`
- Lint/type-check: `flake8`, `mypy`, `black --check .`

## Test Coverage

Quick coverage run (terminal summary):

```bash
poetry run pytest --cov=src --cov-report=term-missing -q
```

Generate an HTML coverage report:

```bash
poetry run pytest --cov=src --cov-report=html -q
open htmlcov/index.html
```

Enforce a minimum coverage threshold (example: 90%):

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=90 -q
```

## Design
- Packages include `__init__.py` to support module discovery and packaging.

## Example Usage Scenarios
## Troubleshooting

- urllib3 NotOpenSSLWarning: Your system Python may be linked to LibreSSL. Use Poetry with Python 3.14 built against OpenSSL (pyenv), or suppress via `PYTHONWARNINGS="ignore::urllib3.exceptions.NotOpenSSLWarning"`.
- Interactive REPL not starting: Ensure you run `python -m src.main` (module mode) so package-relative imports resolve.


Add tasks with smart parsing
```bash
todo add "Complete project @school #high due:2025-10-20 assigned:alice@example.com"
```

```bash
todo add "Call doctor tomorrow at 2pm @personal"
```

Search with regex
```bash
todo search "@work"
```

List and filter
```bash
todo list --priority high
todo list --tag "^school$"
todo list --due "2025-10"
```


- `TaskService` orchestrates parsing and persistence over an in-memory `TodoList`.
- `StorageService` persists tasks to JSON; it accepts both `str` and `Path`.
- Parsers are split into regex patterns, validation, and date parsing utilities.

