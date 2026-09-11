"""Centralized logging configuration.

The project brief explicitly requires that "each test case execution must
include logging of results." pytest's own pass/fail reporting satisfies
part of that, but this module gives every page object and test a proper
`logging.Logger` that writes timestamped, per-step results to both the
console and a persistent log file (logs/test_run.log) - useful evidence
of what actually happened during a run, independent of the HTML report.
"""

import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "test_run.log")

_configured = False


def get_logger(name: str) -> logging.Logger:
    """Returns a module-scoped logger, configuring the shared file/console
    handlers exactly once per test run.
    """
    global _configured
    logger = logging.getLogger(name)

    if not _configured:
        os.makedirs(LOG_DIR, exist_ok=True)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        _configured = True

    return logger
