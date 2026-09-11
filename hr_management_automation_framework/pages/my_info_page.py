"""Page Object for the "My Info" module and its Personal/Contact/etc. tabs."""

from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.authenticated_page import AuthenticatedPage
from utils.logger import get_logger

logger = get_logger(__name__)


class MyInfoPage(AuthenticatedPage):
    """Encapsulates locators/actions for https://.../pim/viewMyDetails
    and its sub-menu tabs (Personal Details, Contact Details, Emergency
    Contacts, and the rest).
    """

    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewMyDetails"
    URL_FRAGMENT = "viewMyDetails"

    # All ten tabs shown under "My Info" on the live site.
    EXPECTED_TABS = [
        "Personal Details",
        "Contact Details",
        "Emergency Contacts",
        "Dependents",
        "Immigration",
        "Job",
        "Salary",
        "Report-to",
        "Qualifications",
        "Memberships",
    ]

    TAB_LINKS = (By.CSS_SELECTOR, "div.orangehrm-tabs-wrapper a")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def load(self) -> "MyInfoPage":
        """Navigates directly to My Info (requires an already-authenticated
        session).
        """
        self.driver.get(self.URL)
        self.is_authenticated_page_loaded()
        return self

    def is_displayed(self) -> bool:
        """Confirms the My Info tab navigation is visible.

        My Info immediately redirects from the generic entry URL to its
        default tab's own route (e.g. .../viewPersonalDetails/empNumber/76),
        which no longer contains "viewMyDetails" as a substring - so
        checking for the tab navigation itself (present on every My Info
        sub-page) is the reliable signal, not the URL.
        """
        return self.is_visible(self.TAB_LINKS, timeout=10)

    def get_tab_names(self) -> List[str]:
        self.find(self.TAB_LINKS)
        return [tab.text.strip() for tab in self.driver.find_elements(*self.TAB_LINKS)]

    def is_tab_visible(self, tab_name: str) -> bool:
        return tab_name in self.get_tab_names()

    def click_tab(self, tab_name: str) -> None:
        for tab in self.driver.find_elements(*self.TAB_LINKS):
            if tab.text.strip() == tab_name:
                tab.click()
                logger.info("Clicked My Info tab '%s'", tab_name)
                return
        raise LookupError(f"My Info tab '{tab_name}' was not found")
