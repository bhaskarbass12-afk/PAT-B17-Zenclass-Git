"""Test-Case-1: Verify whether the URL https://www.guvi.in is valid or
not - the browser should launch and navigate to the given URL and the
web application should load successfully without any error.
"""

from selenium.webdriver.common.by import By

from utils.logger import get_logger

logger = get_logger(__name__)


def test_home_url_is_accessible(home_page):
    """Loads the homepage and confirms the browser actually landed on
    guvi.in (not an error page, a redirect to an unrelated domain, etc.)
    and that the page rendered real content.
    """
    assert "guvi.in" in home_page.driver.current_url, (
        f"Expected to land on guvi.in, got {home_page.driver.current_url!r}"
    )

    body_text = home_page.driver.find_element(By.TAG_NAME, "body").text
    assert body_text.strip(), "Expected the homepage to render visible body content"

    logger.info("Home URL loaded successfully: %s", home_page.driver.current_url)
