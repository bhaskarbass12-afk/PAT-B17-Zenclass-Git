"""Convenience entry point for PyCharm.

PyCharm Community Edition has no built-in runner for .feature files (that
needs the paid Gherkin plugin), but it *can* Run/Debug any plain .py file
with a one-click gutter icon. This script wraps the same Behave CLI
invocation documented in README.md, so right-click > Run 'run_tests' is
enough to execute the whole suite and produce Allure results in
reports/allure-results/.
"""

import sys

from behave.__main__ import main as behave_main


def run() -> int:
    args = [
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", "reports/allure-results",
        "-f", "pretty",
        "features",
    ]
    return behave_main(args)


if __name__ == "__main__":
    sys.exit(run())