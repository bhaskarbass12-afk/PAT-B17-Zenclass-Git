"""Test-Case-1: Validate login functionality using multiple sets of
credentials, driven by a structured external data source (CSV).
"""

import pytest

from data.data_loader import load_login_credentials
from pages.authenticated_page import AuthenticatedPage
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.parametrize(
    "row",
    load_login_credentials(),
    ids=[row["run_id"] for row in load_login_credentials()],
)
def test_login_with_external_dataset(driver, row):
    """For each row in data/login_credentials.csv: attempt login with
    that dataset's username/password, validate the outcome matches the
    row's expected_result, and log out again after every successful
    login.
    """
    logger.info(
        "Run %s (tester=%s, date=%s): attempting login with username='%s'",
        row["run_id"],
        row["tester_name"],
        row["test_date"],
        row["username"],
    )

    login_page = LoginPage(driver).load()
    login_page.login(row["username"], row["password"])

    if row["expected_result"] == "Pass":
        home_page = AuthenticatedPage(driver)
        assert home_page.is_authenticated_page_loaded(), (
            f"[{row['run_id']}] Expected valid credentials to log in successfully"
        )
        logger.info("Run %s: login succeeded as expected", row["run_id"])

        home_page.logout()
        assert login_page.is_displayed(), (
            f"[{row['run_id']}] Expected to be returned to the login page after logout"
        )
        logger.info("Run %s: logout succeeded", row["run_id"])
    else:
        assert login_page.has_error(), (
            f"[{row['run_id']}] Expected invalid credentials to be rejected with an error"
        )
        logger.info(
            "Run %s: login correctly rejected with '%s'",
            row["run_id"],
            login_page.get_error_message(),
        )
