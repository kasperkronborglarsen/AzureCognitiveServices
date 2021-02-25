import sys
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


def get_project_dir() -> Path:
    """Returns the root directory of the project."""
    return Path(__file__).parent.parent.parent


def get_logger(name: str) -> logging.Logger:
    """Returns a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )

    log_dir = get_project_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = RotatingFileHandler(
        str(log_dir / "debug.log"), maxBytes=5000000, backupCount=5
    )
    log_file.setFormatter(log_formatter)
    logger.addHandler(log_file)

    log_console = logging.StreamHandler(sys.stdout)
    log_console.setFormatter(log_formatter)
    logger.addHandler(log_console)

    return logger
