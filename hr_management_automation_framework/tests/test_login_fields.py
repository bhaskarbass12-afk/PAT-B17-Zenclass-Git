"""Test-Case-3: Validate presence of login fields."""

from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


def test_username_and_password_fields_are_visible_and_enabled(driver):
    """The username and password input fields must both be visible and
    enabled for input on the login page.
    """
    login_page = LoginPage(driver).load()

    username_field = login_page.find(login_page.USERNAME_INPUT)
    password_field = login_page.find(login_page.PASSWORD_INPUT)

    assert username_field.is_displayed(), "Expected the username field to be visible"
    assert username_field.is_enabled(), "Expected the username field to be enabled"
    assert password_field.is_displayed(), "Expected the password field to be visible"
    assert password_field.is_enabled(), "Expected the password field to be enabled"

    logger.info("Login fields confirmed visible and enabled")
