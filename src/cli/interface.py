import argparse
from pathlib import Path
from ..services.task_service import TaskService
from ..services.storage_service import StorageService
from ..utils.logger import get_logger, silence_third_party_warnings, set_log_level
import shlex


def make_parser():
    """Create and return the top-level CLI argument parser."""
    p = argparse.ArgumentParser(prog="todo")
    sub = p.add_subparsers(dest="cmd", required=False)
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )
    p.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive mode (REPL)",
    )

    # add
    s_add = sub.add_parser("add")
    s_add.add_argument("raw", type=str, help="Raw task input string")
    s_add.add_argument(
        "--data",
        type=Path,
        default=Path("data/tasks.json"),
        help="Path to tasks json",
    )

    # delete
    s_del = sub.add_parser("delete")
    s_del.add_argument("id", type=int, help="ID of task to delete")
    s_del.add_argument("--data", type=Path, default=Path("data/tasks.json"))

    # update
    s_up = sub.add_parser("update")
    s_up.add_argument("id", type=int, help="ID of task to update")
    s_up.add_argument("raw", type=str, help="Raw task input with new values")
    s_up.add_argument("--data", type=Path, default=Path("data/tasks.json"))

    # list
    s_ls = sub.add_parser("list")
    s_ls.add_argument("--priority", type=str, help="Filter by priority")
    s_ls.add_argument("--tag", type=str, help="Filter by tag pattern")
    s_ls.add_argument("--due", type=str, help="Filter by due-date regex")
    s_ls.add_argument("--data", type=Path, default=Path("data/tasks.json"))

    # complete / incomplete
    s_c = sub.add_parser("complete")
    s_c.add_argument("id", type=int)
    s_c.add_argument("--data", type=Path, default=Path("data/tasks.json"))
    s_ic = sub.add_parser("incomplete")
    s_ic.add_argument("id", type=int)
    s_ic.add_argument("--data", type=Path, default=Path("data/tasks.json"))

    # search
    s_search = sub.add_parser("search")
    s_search.add_argument("pattern", type=str, help="Regex pattern")
    s_search.add_argument("--data", type=Path, default=Path("data/tasks.json"))

    return p


def make_commands_parser():
    """Create a parser for commands only (used by REPL).

    Supports: add, update, delete, list, complete, incomplete, search, exit/quit.
    The REPL uses this to parse each input line without global options.
    """
    p = argparse.ArgumentParser(prog="todo", add_help=False)
    sub = p.add_subparsers(dest="cmd", required=True)

    s_add = sub.add_parser("add")
    s_add.add_argument("raw", type=str)

    s_del = sub.add_parser("delete")
    s_del.add_argument("id", type=int)

    s_up = sub.add_parser("update")
    s_up.add_argument("id", type=int)
    s_up.add_argument("raw", type=str)

    s_ls = sub.add_parser("list")
    s_ls.add_argument("--priority", type=str)
    s_ls.add_argument("--tag", type=str)
    s_ls.add_argument("--due", type=str)

    s_c = sub.add_parser("complete")
    s_c.add_argument("id", type=int)
    s_ic = sub.add_parser("incomplete")
    s_ic.add_argument("id", type=int)

    s_search = sub.add_parser("search")
    s_search.add_argument("pattern", type=str)

    s_exit = sub.add_parser("exit")
    sub.add_parser("quit")

    return p


def execute_command(args: argparse.Namespace, svc: TaskService) -> None:
    """Execute a parsed command against the service.

    Split from main and used by REPL and tests to enable reuse and coverage.
    """
    match args.cmd:
        case "add":
            t = svc.add(args.raw)
            print(f"Added task #{t.id}: {t.description}")
        case "delete":
            ok = svc.delete(args.id)
            print("Deleted." if ok else "No such task.")
        case "update":
            ok = svc.update(args.id, args.raw)
            print("Updated." if ok else "No such task.")
        case "list":
            tasks = svc.list_all()
            if getattr(args, "priority", None):
                tasks = svc.filter_by_priority(args.priority)
            if getattr(args, "tag", None):
                tasks = svc.filter_by_tag(args.tag)
            if getattr(args, "due", None):
                tasks = svc.filter_by_due(args.due)
            for t in tasks:
                status = "✓" if t.completed else " "
                print(
                    f"[{status}] {t.id}: {t.description} (tags: {t.tags}) "
                    f"due: {t.due_date}"
                )
        case "complete":
            ok = svc.mark_complete(args.id)
            print("Marked complete." if ok else "No such task.")
        case "incomplete":
            ok = svc.mark_incomplete(args.id)
            print("Marked incomplete." if ok else "No such task.")
        case "search":
            results = svc.search(args.pattern)
            for t in results:
                print(f"{t.id}: {t.description} (tags: {t.tags})")


def run_repl(svc: TaskService, logger) -> None:
    """Simple interactive REPL for entering commands without restarting.

    Prints a short help line and processes commands until the user exits.
    """
    print("Interactive mode. Type 'help' for commands, 'exit' to quit.")
    cmd_parser = make_commands_parser()
    while True:
        try:
            line = input("todo> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line.lower() in {"exit", "quit"}:
            break
        if line.lower() in {"help", "?"}:
            print("Commands: add, update, delete, list [--priority P --tag REGEX --due PATTERN],")
            print("          complete ID, incomplete ID, search PATTERN, exit")
            continue
        try:
            tokens = shlex.split(line)
            args = cmd_parser.parse_args(tokens)
            # execute
            execute_command(args, svc)
        except SystemExit:
            logger.warning("Invalid command. Type 'help' for usage.")
        except Exception as exc:
            logger.error("Error: %s", exc)


def main():
    """Entry point for the CLI application."""
    parser = make_parser()
    args = parser.parse_args()

    # Configure root logger level based on CLI flag (handlers set in util)
    silence_third_party_warnings()
    import os
    os.environ["LOG_LEVEL"] = args.log_level
    set_log_level(args.log_level)
    logger = get_logger("todo.cli")
    logger.info("Starting CLI with log level %s", args.log_level)

    # Allow per-command override of storage path
    data_path = getattr(args, "data", Path("data/tasks.json"))
    storage = StorageService(data_path)
    svc = TaskService(storage)
    # Interactive mode if requested or if no subcommand provided
    if getattr(args, "interactive", False) or not getattr(args, "cmd", None):
        run_repl(svc, logger)
        return

    execute_command(args, svc)


if __name__ == "__main__":
    main()
