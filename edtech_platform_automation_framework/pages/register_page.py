"""Page Object for the GUVI registration page (https://www.guvi.in/register/)."""

from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class RegisterPage(BasePage):
    """Encapsulates the page reached by clicking the header's "Sign up"
    button. The brief's Test-Case-4 and Test-Case-5 both boil down to
    confirming this same navigation, so this page object is kept
    intentionally minimal - just enough to confirm arrival.
    """

    URL_FRAGMENT = "register"

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def is_displayed(self) -> bool:
        return self.wait_until_url_contains(self.URL_FRAGMENT)
