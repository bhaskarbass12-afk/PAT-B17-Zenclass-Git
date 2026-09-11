"""Shared pytest fixtures for the HR Management automation suite.

`driver` owns the WebDriver lifecycle for each test: a fresh browser
session per test function, always quit in teardown via a try/finally -
this guarantees the browser is properly closed after every test case,
even if the test body raises.

Supports the brief's "executed across multiple browsers" requirement via
a `--browser` CLI option (defaults to chrome; also supports firefox).
"""

import os
import sys
from pathlib import Path

# Make sure the project root (the parent of this tests/ folder) is on
# sys.path regardless of how pytest resolves its rootdir/ini file in a
# given environment. This project's pytest.ini also sets
# `pythonpath = .` for the same purpose, but that setting depends on
# pytest correctly identifying this project's own pytest.ini as its
# config file - if a shared virtual environment or IDE run configuration
# ever causes a different rootdir to be picked (e.g. when several
# unrelated projects share one venv), the `from data...` / `from
# pages...` imports below would otherwise fail with a
# `ModuleNotFoundError` even though the code itself is correct. This
# explicit insert is a hard guarantee that doesn't depend on any of
# that.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from data.users import ADMIN_PASSWORD, ADMIN_USERNAME
from pages.login_page import LoginPage


def pytest_addoption(parser):
    # Named "--target-browser" (not the more obvious "--browser") on
    # purpose: several other pytest plugins (pytest-playwright,
    # pytest-selenium) register their own built-in "--browser" option
    # the moment they're installed anywhere in the active virtual
    # environment - even one shared across unrelated projects - which
    # collides with a same-named custom option and crashes pytest at
    # startup with "conflicting option string: --browser". Using a
    # project-specific name avoids that regardless of what else is
    # installed alongside this project.
    parser.addoption(
        "--target-browser",
        action="store",
        default="chrome",
        help="Browser to run the suite against: chrome (default) or firefox",
    )


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--target-browser").lower()
    headless = os.getenv("HEADLESS", "true").lower() != "false"

    if browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        drv = webdriver.Firefox(options=options)
    else:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        drv = webdriver.Chrome(options=options)

    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture
def admin_login(driver):
    """Logs in as Admin and returns the driver, ready for any
    authenticated page object to be constructed against it.
    """
    LoginPage(driver).load().login(ADMIN_USERNAME, ADMIN_PASSWORD)
    return driver
