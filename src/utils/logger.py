import logging
import os
import sys
import warnings


_LEVEL_TO_COLOR = {
    "DEBUG": "\x1b[36m",    # cyan
    "INFO": "\x1b[32m",     # green
    "WARNING": "\x1b[33m",  # yellow
    "ERROR": "\x1b[31m",    # red
    "CRITICAL": "\x1b[35m", # magenta
}
_RESET = "\x1b[0m"


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt: str, datefmt: str | None = None, use_color: bool = True):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.use_color = use_color and (os.getenv("NO_COLOR") is None)

    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        if self.use_color and levelname in _LEVEL_TO_COLOR:
            record.levelname = f"{_LEVEL_TO_COLOR[levelname]}{levelname}{_RESET}"
            record.name = f"{_LEVEL_TO_COLOR[levelname]}{record.name}{_RESET}"
        try:
            return super().format(record)
        finally:
            record.levelname = levelname


def _build_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    stream = getattr(handler, "stream", sys.stderr)
    use_color = hasattr(stream, "isatty") and stream.isatty()
    formatter = ColorFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        use_color=use_color,
    )
    handler.setFormatter(formatter)
    return handler


def set_log_level(level_str: str) -> None:
    level = getattr(logging, level_str.upper(), logging.INFO)
    logging.getLogger().setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger with a consistent timestamped (colored) format.

    Respects LOG_LEVEL env var (default INFO). Suitable for both app and tests.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)
    logger.setLevel(level)

    handler = _build_handler()
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def silence_third_party_warnings() -> None:
    """Silence noisy third-party warnings (e.g., urllib3 NotOpenSSLWarning)."""
    try:
        from urllib3.exceptions import NotOpenSSLWarning  # type: ignore

        warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
        # Silence other urllib3 warnings broadly
        warnings.filterwarnings("ignore", module=r"urllib3\..*")
    except Exception:
        # urllib3 may not be installed; ignore
        pass



