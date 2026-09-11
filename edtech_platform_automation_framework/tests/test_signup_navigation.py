"""Test-Case-5: Verify navigation to the Sign-Up page via the Sign-Up
button, and validate the redirected page URL.

This is deliberately a separate test case from Test-Case-4 (per the
brief) even though it exercises the same click - Test-Case-4 focuses on
the button itself (visible/clickable), this one focuses specifically on
validating the destination: the redirected URL must contain
https://www.guvi.in/register/ and that page must load successfully.
"""

from selenium.webdriver.common.by import By

from pages.register_page import RegisterPage
from utils.exceptions import NavigationError
from utils.logger import get_logger

logger = get_logger(__name__)


def test_signup_navigation_lands_on_register_page(home_page):
    home_page.click_signup_button()

    register_page = RegisterPage(home_page.driver)
    if not register_page.is_displayed():
        raise NavigationError(
            f"Expected the Sign-Up button to navigate to a URL containing "
            f"'register', but landed on {home_page.driver.current_url!r}"
        )

    assert "https://www.guvi.in/register" in home_page.driver.current_url, (
        f"Expected redirected URL to start with 'https://www.guvi.in/register', "
        f"got {home_page.driver.current_url!r}"
    )

    body_text = home_page.driver.find_element(By.TAG_NAME, "body").text
    assert body_text.strip(), "Expected the register page to load with visible content"

    logger.info("Sign-Up navigation confirmed at: %s", home_page.driver.current_url)
