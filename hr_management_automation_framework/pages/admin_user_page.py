"""Page Objects for Admin > User Management: the system users list and
the "Add User" form.
"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.authenticated_page import AuthenticatedPage
from utils.exceptions import UserManagementError
from utils.logger import get_logger

logger = get_logger(__name__)


class AddUserPage(AuthenticatedPage):
    """Encapsulates the "Add User" form reached from Admin > User
    Management > Add.
    """

    URL_FRAGMENT = "saveSystemUser"

    SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and contains(.,'Save')]")
    TOAST = (By.CSS_SELECTOR, ".oxd-toast-content")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def is_displayed(self) -> bool:
        return self.wait_until_url_contains(self.URL_FRAGMENT)

    def create_user(
        self,
        user_role: str,
        employee_search_text: str,
        status: str,
        username: str,
        password: str,
    ) -> None:
        """Fills in and submits the Add User form."""
        self.select_dropdown("User Role", user_role)
        self.select_autocomplete_suggestion("Employee Name", employee_search_text)
        self.select_dropdown("Status", status)
        self.type_into_field("Username", username)
        self.type_into_field("Password", password)
        self.type_into_field("Confirm Password", password)
        self.click(self.SAVE_BUTTON)
        logger.info("Submitted new user '%s' (role=%s, status=%s)", username, user_role, status)

    def get_save_confirmation(self) -> str:
        if not self.is_visible(self.TOAST, timeout=10):
            raise UserManagementError("Expected a confirmation toast after saving the new user")
        return self.get_text(self.TOAST)


class AdminUserListPage(AuthenticatedPage):
    """Encapsulates Admin > User Management > System Users (the list and
    search filter).
    """

    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers"
    URL_FRAGMENT = "viewSystemUsers"

    ADD_BUTTON = (By.XPATH, "//button[contains(.,'Add')]")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
    NO_RECORDS_MESSAGE = (By.CSS_SELECTOR, ".oxd-text--span")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def load(self) -> "AdminUserListPage":
        """Navigates directly to the System Users list (requires an
        already-authenticated session).
        """
        self.driver.get(self.URL)
        self.is_authenticated_page_loaded()
        return self

    def is_displayed(self) -> bool:
        return self.wait_until_url_contains(self.URL_FRAGMENT)

    def click_add(self) -> AddUserPage:
        self.click(self.ADD_BUTTON)
        self.wait_until_url_contains(AddUserPage.URL_FRAGMENT)
        return AddUserPage(self.driver, self.timeout)

    def search_by_username(self, username: str) -> None:
        self.type_into_field("Username", username)
        self.click(self.SEARCH_BUTTON)
        logger.info("Searched system users for username '%s'", username)

    def is_user_listed(self, username: str, timeout: int = 10) -> bool:
        """Waits (rather than checking just once) for `username` to
        appear in the results table - the table takes a moment to
        re-render after Search is clicked, so an instant one-shot check
        can run before the filtered results actually land.
        """
        try:
            self._wait(timeout).until(
                lambda d: any(username in row.text for row in d.find_elements(*self.TABLE_ROWS))
            )
            return True
        except TimeoutException:
            return False
