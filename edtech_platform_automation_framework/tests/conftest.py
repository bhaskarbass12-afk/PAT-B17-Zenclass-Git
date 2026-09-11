"""Shared pytest fixtures for the EdTech platform automation suite.

`driver` owns the WebDriver lifecycle for each test: a fresh browser
session per test function, always quit in teardown via a try/finally -
this guarantees the browser is properly closed after every test case,
even if the test body raises.

Supports the brief's "cross-browser" requirement via a `--target-browser`
CLI option (defaults to chrome; also supports firefox). It's deliberately
NOT named the more obvious "--browser": that name collides with a
built-in option some other pytest plugins (pytest-playwright,
pytest-selenium) register automatically the moment they're installed
anywhere in the active virtual environment - a real, previously-hit
issue when this same kind of option collided across sibling projects
sharing one venv.
"""

import os
import sys
from pathlib import Path

# Guarantee the project root is importable regardless of how pytest
# resolves its rootdir/ini file in a given environment (see the
# hr_management_automation_framework project's README for the exact
# failure mode this avoids).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from data.users import VALID_EMAIL, VALID_PASSWORD
from pages.home_page import HomePage
from pages.login_page import LoginPage

# Loads GUVI_EMAIL / GUVI_PASSWORD from a local .env file (see
# .env.example). The .env file is git-ignored; never commit real
# credentials.
load_dotenv()


def pytest_addoption(parser):
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
def home_page(driver):
    """A freshly loaded HomePage."""
    return HomePage(driver).load()


@pytest.fixture
def login_page(driver):
    """A freshly loaded LoginPage."""
    return LoginPage(driver).load()


@pytest.fixture
def valid_credentials():
    """Real GUVI credentials, read from environment/.env.

    Tests that require an actual successful login are skipped (not
    failed) when credentials aren't configured, so the rest of the
    suite can still run without them.
    """
    if not VALID_EMAIL or not VALID_PASSWORD:
        pytest.skip(
            "GUVI_EMAIL / GUVI_PASSWORD not set. Copy .env.example to .env "
            "and fill in a real GUVI account login to run this test."
        )
    return VALID_EMAIL, VALID_PASSWORD


@pytest.fixture
def logged_in_home_page(driver, login_page, valid_credentials):
    """Logs in with a real account and returns a HomePage bound to the
    same driver, ready for any test that needs to start from an
    authenticated session (e.g. logout).
    """
    email, password = valid_credentials
    login_page.login(email, password)
    return HomePage(driver)
