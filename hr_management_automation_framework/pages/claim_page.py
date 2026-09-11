"""Page Objects for the Claim module and its "Submit Claim" form.

The task brief describes the scenario generically as "entering details
like claim type, amount, and reason." OrangeHRM's actual Submit Claim
screen creates the claim record from an Event (claim type), Currency, and
Remarks (reason); the itemized amount is added as an expense line on the
claim's detail page immediately afterward. This page object models both
steps so the resulting workflow still covers "claim type", "amount", and
"reason" end to end.
"""

from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.authenticated_page import AuthenticatedPage
from utils.exceptions import ClaimSubmissionError
from utils.logger import get_logger

logger = get_logger(__name__)


class ClaimModulePage(AuthenticatedPage):
    """Encapsulates the Claim module's landing page (My Claims / claim
    list) and its "Submit Claim" action.
    """

    URL_FRAGMENT = "claim"
    CLAIM_LIST_ROWS = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def is_displayed(self) -> bool:
        return self.wait_until_url_contains(self.URL_FRAGMENT)

    def open_submit_claim(self) -> "SubmitClaimPage":
        submit_claim_link = (By.XPATH, "//a[normalize-space(text())='Submit Claim']")
        self.click(submit_claim_link)
        return SubmitClaimPage(self.driver, self.timeout)

    def get_claim_list_row_count(self) -> int:
        return len(self.driver.find_elements(*self.CLAIM_LIST_ROWS))


class SubmitClaimPage(AuthenticatedPage):
    """Encapsulates the "Submit Claim" creation form (Event, Currency,
    Remarks) and the resulting claim-detail page where an expense line
    (with an amount) is added.
    """

    CREATE_BUTTON = (By.XPATH, "//button[@type='submit' and contains(.,'Create')]")
    ADD_EXPENSE_BUTTON = (By.XPATH, "//button[contains(.,'Add')]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(.,'Submit')]")
    TOAST = (By.CSS_SELECTOR, ".oxd-toast-content")
    EXPENSE_DIALOG = (By.CSS_SELECTOR, ".oxd-dialog-container-default")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def create_claim(self, remarks: str) -> str:
        """Selects the first available Event and Currency, fills in
        Remarks (the "reason"), and creates the claim record. Returns the
        Event name that was selected (the "claim type").
        """
        event = self.select_first_dropdown_option("Event")
        self.select_first_dropdown_option("Currency")
        if self.is_visible((By.XPATH, "//label[normalize-space(text())='Remarks']"), timeout=3):
            self.type_into_field("Remarks", remarks)
        self.click(self.CREATE_BUTTON)
        logger.info("Created claim (event=%s)", event)
        return event

    def add_expense(self, amount: str) -> None:
        """Adds an expense line item with the given amount to the claim
        that was just created, if the "Add" action is available on this
        instance's claim-detail page.
        """
        if not self.is_clickable(self.ADD_EXPENSE_BUTTON, timeout=5):
            logger.info("No 'Add expense' action available; skipping amount entry")
            return
        self.click(self.ADD_EXPENSE_BUTTON)
        if self.is_visible((By.XPATH, "//label[normalize-space(text())='Amount']"), timeout=5):
            # The "Add Expense" modal also requires an Expense Type and a
            # Date (both left empty produce "Required" validation errors
            # that silently keep the modal open when "Save" is clicked) -
            # not just the Amount the task brief calls out explicitly.
            # Date uses this instance's yyyy-dd-mm format, same as the
            # Assign Leave form; today's date is always a valid choice.
            self.select_first_dropdown_option("Expense Type")
            today_yyyy_dd_mm = date.today().strftime("%Y-%d-%m")
            self.type_into_field("Date", today_yyyy_dd_mm)
            self.type_into_field("Amount", amount)
            save_locator = (By.XPATH, "//button[@type='submit']")
            self.click(save_locator)
            # The "Add expense" action opens a modal dialog; its overlay
            # can still be closing when the next action (submitting the
            # claim for approval) tries to click a button behind it,
            # intercepting that click. Waiting for the dialog itself to
            # disappear avoids that race.
            self.wait_until_invisible(self.EXPENSE_DIALOG, timeout=10)
            logger.info("Added expense line item with amount %s", amount)

    def submit_for_approval(self) -> None:
        if self.is_clickable(self.SUBMIT_BUTTON, timeout=5):
            self.click(self.SUBMIT_BUTTON)
            logger.info("Submitted claim for approval")

    def get_confirmation(self) -> str:
        if not self.is_visible(self.TOAST, timeout=10):
            raise ClaimSubmissionError("Expected a confirmation toast after creating the claim")
        return self.get_text(self.TOAST)
