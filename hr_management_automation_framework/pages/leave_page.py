"""Page Objects for the Leave module and its "Assign Leave" form."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.authenticated_page import AuthenticatedPage
from utils.exceptions import LeaveAssignmentError
from utils.logger import get_logger

logger = get_logger(__name__)


class LeaveModulePage(AuthenticatedPage):
    """Encapsulates the Leave module's landing page and its "Assign
    Leave" tab.
    """

    URL_FRAGMENT = "leave"

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def is_displayed(self) -> bool:
        return self.wait_until_url_contains(self.URL_FRAGMENT)

    def open_assign_leave(self) -> "AssignLeavePage":
        assign_leave_link = (By.XPATH, "//a[normalize-space(text())='Assign Leave']")
        self.click(assign_leave_link)
        return AssignLeavePage(self.driver, self.timeout)


class AssignLeavePage(AuthenticatedPage):
    """Encapsulates the Assign Leave form (Employee Name, Leave Type,
    From Date, To Date).
    """

    URL_FRAGMENT = "assignLeave"
    ASSIGN_BUTTON = (By.XPATH, "//button[@type='submit' and contains(.,'Assign')]")
    TOAST = (By.CSS_SELECTOR, ".oxd-toast-content")
    # This demo's employees generally carry a 0-day balance for most leave
    # types, so submitting almost always raises OrangeHRM's own "Employee
    # does not have sufficient leave balance... Click OK to confirm"
    # dialog rather than saving immediately. Confirming it is what a real
    # admin would do to intentionally override the balance check, so the
    # form isn't actually saved until this optional dialog (when present)
    # is dismissed with "Ok".
    # Note: the button's visible text lives in a child <span>, so
    # `normalize-space()` (the button's full string-value) must be used
    # instead of `normalize-space(text())` (only direct text nodes),
    # which matches nothing here.
    CONFIRM_DIALOG_OK_BUTTON = (By.XPATH, "//button[normalize-space()='Ok']")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def is_displayed(self) -> bool:
        return self.wait_until_url_contains(self.URL_FRAGMENT)

    def assign_leave(self, employee_search_text: str, from_date: str, to_date: str) -> str:
        """Fills in and submits the Assign Leave form.

        The specific set of Leave Types available is demo-data-dependent,
        so the first real option is selected automatically (and returned)
        rather than assuming a fixed leave type name exists.

        Dates are passed through as-is (expected format: yyyy-mm-dd,
        matching this OrangeHRM instance's configured date format).
        """
        self.select_autocomplete_suggestion("Employee Name", employee_search_text)
        leave_type = self.select_first_dropdown_option("Leave Type")
        self.type_into_field("From Date", from_date)
        self.type_into_field("To Date", to_date)
        self.click(self.ASSIGN_BUTTON)

        if self.is_visible(self.CONFIRM_DIALOG_OK_BUTTON, timeout=5):
            logger.info("Insufficient-balance confirmation dialog shown; confirming with 'Ok'")
            self.click(self.CONFIRM_DIALOG_OK_BUTTON)

        logger.info(
            "Assigned leave to '%s' (type=%s, %s - %s)",
            employee_search_text,
            leave_type,
            from_date,
            to_date,
        )
        return leave_type

    def get_confirmation(self) -> str:
        if not self.is_visible(self.TOAST, timeout=10):
            raise LeaveAssignmentError("Expected a confirmation toast after assigning leave")
        return self.get_text(self.TOAST)
