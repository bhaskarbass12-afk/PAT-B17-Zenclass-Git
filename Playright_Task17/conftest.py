import os

import pytest
from dotenv import load_dotenv

from dashboard_page import DashboardPage
from login_page import LoginPage

# Load ZEN_EMAIL / ZEN_PASSWORD from a local .env file (see .env.example).
# The .env file is git-ignored; never commit real credentials.
load_dotenv()


@pytest.fixture
def valid_credentials():

    email = os.getenv("ZEN_EMAIL")
    password = os.getenv("ZEN_PASSWORD")
    if not email or not password:
        pytest.skip(
            "ZEN_EMAIL / ZEN_PASSWORD not set. Copy .env.example to .env and "
            "fill in a real Zen Portal login to run this test."
        )
    return email, password


@pytest.fixture
def login_page(page):

    return LoginPage(page).load()


@pytest.fixture
def dashboard_page(page):

    return DashboardPage(page)
