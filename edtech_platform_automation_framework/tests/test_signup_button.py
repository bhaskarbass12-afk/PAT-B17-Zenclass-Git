"""Test-Case-4: Verify visibility and clickability of the Sign-Up button.

Scenario: check if the Sign-Up button is displayed, and ensure the
Sign-Up button is clickable - on clicking, it should redirect to
https://www.guvi.in/register/.
"""

from pages.register_page import RegisterPage
from utils.logger import get_logger

logger = get_logger(__name__)


def test_signup_button_visible_and_redirects(home_page):
    assert home_page.is_any_visible(home_page.SIGNUP_BUTTON), (
        "Expected the header 'Sign up' button to be visible"
    )

    home_page.click_signup_button()

    register_page = RegisterPage(home_page.driver)
    assert register_page.is_displayed(), (
        "Expected clicking 'Sign up' to redirect to the register page"
    )
    assert "guvi.in/register" in home_page.driver.current_url, (
        f"Expected the redirected URL to contain 'guvi.in/register', "
        f"got {home_page.driver.current_url!r}"
    )
    logger.info("Sign up button redirected to: %s", home_page.driver.current_url)
