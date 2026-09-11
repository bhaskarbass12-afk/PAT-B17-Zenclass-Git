"""Shared base class for every page that appears *after* login.

Every authenticated OrangeHRM page has the same persistent header: the
main sidebar menu (Admin, PIM, Leave, Time, Recruitment, My Info,
Performance, Dashboard, ...) and the user dropdown (which contains
Logout). Rather than duplicating menu/logout locators across
`MyInfoPage`, `AdminUserListPage`, `LeavePage`, `ClaimPage`, etc., they
all inherit this class.
"""

from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class AuthenticatedPage(BasePage):
    """Common header (main menu + user dropdown) shared by every
    authenticated page.
    """

    DASHBOARD_URL_FRAGMENT = "dashboard"

    MENU_ITEM_LINKS = (By.CSS_SELECTOR, "a.oxd-main-menu-item")
    USER_DROPDOWN_TAB = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def is_authenticated_page_loaded(self) -> bool:
        """Waits until the main menu (present on every authenticated
        page) has rendered.
        """
        return len(self.find_menu_items()) > 0

    def find_menu_items(self):
        self.find(self.MENU_ITEM_LINKS)
        return self.driver.find_elements(*self.MENU_ITEM_LINKS)

    def get_menu_item_names(self) -> List[str]:
        return [item.text.strip() for item in self.find_menu_items()]

    def is_menu_item_visible(self, name: str) -> bool:
        return name in self.get_menu_item_names()

    def is_menu_item_clickable(self, name: str) -> bool:
        for item in self.find_menu_items():
            if item.text.strip() == name:
                return item.is_enabled() and item.is_displayed()
        return False

    def click_menu_item(self, name: str) -> None:
        """Clicks the main-menu item whose visible text matches `name`
        exactly (e.g. "Admin", "PIM", "Leave", "My Info").
        """
        for item in self.find_menu_items():
            if item.text.strip() == name:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", item)
                item.click()
                logger.info("Clicked main menu item '%s'", name)
                return
        raise LookupError(f"Main menu item '{name}' was not found")

    def logout(self) -> None:
        """Logs out via the user dropdown in the top-right corner."""
        self.click(self.USER_DROPDOWN_TAB)
        logout_link = (By.XPATH, "//a[normalize-space(text())='Logout']")
        self.click(logout_link)
        logger.info("Logged out")
