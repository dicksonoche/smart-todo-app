# Architecture Overview

- CLI (`cli.interface`) consumes `TaskService` for all operations.
- `TaskService` orchestrates parsing (`parsers/*`), in-memory list (`models.TodoList`), and persistence (`services.StorageService`).
- `Task` is a dataclass with JSON serialization methods.
- Regex patterns are centralized in `parsers.regex_patterns` and used by parser and validator modules.

## Project Board Workflow

- Backlog / To Do / In Progress / Code Review / Done
  - What: Issue tracking and workflow columns for development.
  - Where: GitHub Project board on your fork; issues in your forked repo.
  - How:
    - Create issues: [FEATURE] Implement regex task parser, [FEATURE] Add task CRUD, [FEATURE] Implement search with regex, [FEATURE] Date validation with regex, [FEATURE] Tag extraction system, [BUG] Fix date parsing edge case, [TEST] Add unit tests for regex patterns.
    - Move cards across columns as work progresses and link PRs to issues.
    - Branching: develop on `feature/*` branches; open PRs to your fork's `main`.

## Core Features

- Add, update, delete, list tasks
  - What: CRUD over tasks.
  - Where:
    - Service: `src/services/task_service.py` (`add`, `update`, `delete`, `list_all`).
    - Model: `src/models/task.py`, `src/models/todo_list.py`.
    - CLI: `src/cli/interface.py` subcommands `add`, `update`, `delete`, `list`.
  - How (CLI):
    - `todo add "Buy milk @home #high"`
    - `todo update 2 "Call mom tomorrow @family"`
    - `todo delete 3`
    - `todo list [--priority high] [--tag "^home$"] [--due "2025-10"]`

- Mark complete/incomplete
  - What: Toggle completion state.
  - Where: `src/models/todo_list.py` (`mark_complete`, `mark_incomplete`), orchestrated by `src/services/task_service.py`.
  - How (CLI): `todo complete 1`, `todo incomplete 1`.

- Smart parsing with regex
  - What: Extract description, tags, priority, due dates, email, time.
  - Where:
    - Patterns: `src/parsers/regex_patterns.py`.
    - Parser: `src/parsers/task_parser.py` (uses `parse_due_date`, `validate_*`).
    - Dates: `src/parsers/date_parser.py` (supports `due:YYYY-MM-DD`, `tomorrow`, `next week`, and natural tokens without `due:`).
    - Validation: `src/parsers/validator.py` (`validate_email`, `validate_priority`, `validate_tag`, `validate_date`, `validate_task_id`).
  - How:
    - Input example: `"Buy groceries @shopping #high due:2025-10-20 assigned:alice@example.com"`.
    - The CLI `add` and `update` route raw text through `TaskService.add/update` → `parse_task_input`.

- Regex search and filtering
  - What: Search descriptions and tags; filter by tag regex and due-date patterns.
  - Where: `src/services/task_service.py` (`search`, `filter_by_tag`, `filter_by_due`, `filter_by_priority`).
  - How (CLI):
    - `todo search "grocer|milk"`
    - `todo list --tag "^work$"`
    - `todo list --due "2025-10"`
    - `todo list --priority high`

- JSON persistence
  - What: File-backed storage of tasks in JSON format.
  - Where: `src/services/storage_service.py`.
  - How:
    - Default path: `data/tasks.json` (auto-created).
    - Override path per command with `--data PATH`.
    - Serialization via `Task.to_dict()` / `Task.from_dict()`.

## Entry Points

- CLI entry: `src/main.py` (runs `cli.interface.main`).
- Programmatic: import `TaskService` from `src/services/task_service.py` and use its methods.

## Interactive CLI (REPL)

- Start with `--interactive` or no subcommand. The REPL uses a dedicated commands parser and executes through the same `TaskService` methods as non-interactive mode. It supports `add`, `update`, `delete`, `list`, `complete`, `incomplete`, `search`, and `exit`.

## Logging & Timestamps

- Logging: centralized in `src/utils/logger.py` with colored, timestamped output. Configure via `--log-level` or `LOG_LEVEL` env var. Tests default to WARNING in `tests/conftest.py`.
- Timestamps: `Task` records `created_at` and `updated_at` (ISO strings in JSON). `updated_at` is set on updates.