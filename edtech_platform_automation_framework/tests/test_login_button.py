"""Test-Case-3: Verify visibility and clickability of the Login button.

Scenario: check if the Login button is displayed, and ensure the Login
button is clickable (clicking it should navigate to the login page).
"""

from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


def test_login_button_visible_and_clickable(home_page):
    assert home_page.is_any_visible(home_page.LOGIN_BUTTON), (
        "Expected the header 'Login' button to be visible"
    )

    home_page.click_login_button()

    login_page = LoginPage(home_page.driver)
    assert login_page.is_displayed(), (
        "Expected clicking 'Login' to navigate to the sign-in page"
    )
    logger.info("Login button navigated to: %s", home_page.driver.current_url)
