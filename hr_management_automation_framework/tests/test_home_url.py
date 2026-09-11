"""Test-Case-2: Verify that the home URL is accessible."""

from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


def test_home_url_is_accessible(driver):
    """Launches the browser and navigates to the application's home URL;
    the login page should load without error.
    """
    login_page = LoginPage(driver).load()

    assert login_page.is_displayed(), "Expected the login page to load without error"
    logger.info("Home URL loaded successfully: %s", driver.current_url)
