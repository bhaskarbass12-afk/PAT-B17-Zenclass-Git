"""Page Object for the GUVI homepage (https://www.guvi.in/)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """Encapsulates the homepage: the URL/title checks, and the header
    nav items ("LIVE Classes", "Courses", "Practice", ...) that the
    brief calls out by name.
    """

    URL = "https://www.guvi.in"

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def load(self) -> "HomePage":
        self.driver.get(self.URL)
        logger.info("Loaded home page: %s", self.URL)
        return self

    def get_title(self) -> str:
        return self.driver.title

    def is_menu_item_visible(self, item_text: str) -> bool:
        """True if a top-nav item with this exact visible text (e.g.
        "Courses", "LIVE Classes", "Practice") is displayed. Uses
        `first_visible`'s duplicate-filtering under the hood since this
        site renders a hidden mobile copy of every nav item alongside
        the visible desktop one.
        """
        locator = (By.XPATH, f"//p[normalize-space(text())='{item_text}']")
        return self.is_any_visible(locator, timeout=5)
