"""Base Page Object shared by every page in the framework.

This is the core of the framework's OOP design. Every concrete page
inherits explicit-wait helpers, exception handling, and - importantly for
this app - a generic "find the field/dropdown next to this visible
label" mechanism.

OrangeHRM's UI (built on its "oxd" component library) consistently
structures every form field the same way:

    <div class="oxd-input-group">
        <label class="oxd-label">Employee Name</label>
        <div>...<input> or .oxd-select-text...</div>
    </div>

So rather than hardcoding a different brittle locator for every field on
every page (Add User, Assign Leave, Submit Claim all reuse this same
structure), every page object drives its forms through `type_into_field`
and `select_dropdown`, keyed by the field's visible label text - the same
"locate by what a human sees" principle used for products-by-name in the
e-commerce framework.
"""

from typing import Optional, Tuple

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.exceptions import ElementInteractionError
from utils.logger import get_logger

DEFAULT_TIMEOUT = 15

Locator = Tuple[str, str]

logger = get_logger(__name__)


class BasePage:
    """Common explicit-wait, error-handling, and labeled-form helpers for
    all page objects.
    """

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.timeout)

    # -- Generic explicit-wait helpers -----------------------------------

    def find(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        try:
            return self._wait(timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException as exc:
            raise ElementInteractionError(
                f"Element {locator} was not visible after {timeout or self.timeout}s"
            ) from exc

    def click(self, locator: Locator, timeout: Optional[int] = None) -> None:
        try:
            element = self._wait(timeout).until(EC.element_to_be_clickable(locator))
            element.click()
        except StaleElementReferenceException:
            element = self._wait(timeout).until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException as exc:
            raise ElementInteractionError(
                f"Element {locator} was not clickable after {timeout or self.timeout}s"
            ) from exc

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        return self.find(locator, timeout).text

    def is_visible(self, locator: Locator, timeout: int = 3) -> bool:
        """Non-raising visibility check. Uses a short default timeout so
        an absent element doesn't stall a test for the full page-load
        timeout.
        """
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_clickable(self, locator: Locator, timeout: int = 3) -> bool:
        try:
            self._wait(timeout).until(EC.element_to_be_clickable(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_until_invisible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """Waits until `locator` is no longer visible (or is gone from
        the DOM). Used after dismissing a modal/dialog so a subsequent
        click on a page element behind it doesn't get intercepted by the
        dialog's own overlay while it's still closing.
        """
        try:
            return bool(self._wait(timeout).until(EC.invisibility_of_element_located(locator)))
        except TimeoutException:
            return False

    def wait_until_url_contains(self, fragment: str, timeout: Optional[int] = None) -> bool:
        try:
            return bool(self._wait(timeout).until(EC.url_contains(fragment)))
        except TimeoutException:
            return False

    def wait_until_url_changes(self, previous_url: str, timeout: Optional[int] = None) -> bool:
        """Waits until the current URL differs from `previous_url` - used
        after an action whose destination URL isn't known in advance
        (e.g. clicking a My Info tab, or submitting a form that may
        succeed or fail down different routes).
        """
        try:
            return bool(self._wait(timeout).until(lambda d: d.current_url != previous_url))
        except TimeoutException:
            return False

    # -- Labeled-field helpers (OrangeHRM's "oxd-input-group" pattern) ---

    def _label_container(self, label_text: str, timeout: Optional[int] = None) -> WebElement:
        """Returns the `.oxd-input-group` wrapper for the field whose
        visible label matches `label_text` exactly.
        """
        # Note the space-padded `contains()` check: a naive
        # `contains(@class,'oxd-input-group')` also matches the much
        # smaller `oxd-input-group__label-wrapper` div (since that class
        # name starts with the same substring), which only wraps the
        # label itself and not the field's actual input/select control.
        # Padding both sides with spaces requires "oxd-input-group" to
        # match as a whole class *token*, not a prefix of a longer one.
        locator = (
            By.XPATH,
            f"//label[normalize-space(text())='{label_text}']"
            "/ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' oxd-input-group ')][1]",
        )
        return self.find(locator, timeout)

    def _find_child(
        self, container: WebElement, by: str, value: str, timeout: Optional[int] = None
    ) -> WebElement:
        """Waits for a child element to appear *within an already-found
        container*, rather than assuming it's already there.

        The label wrapping a field can render a moment before the
        field's own input/select control finishes mounting (a real
        React/Vue hydration timing gap observed against the live site) -
        a plain `container.find_element(...)` can lose that race. Polling
        via WebDriverWait until the child actually resolves avoids it.
        """
        try:
            return self._wait(timeout).until(lambda _: container.find_element(by, value))
        except TimeoutException as exc:
            raise ElementInteractionError(
                f"Child element {by}={value!r} did not appear within the field's "
                f"container after {timeout or self.timeout}s"
            ) from exc

    def type_into_field(self, label_text: str, value: str, timeout: Optional[int] = None) -> None:
        """Types `value` into the text/autocomplete input located next to
        the field labeled `label_text`.

        Some of OrangeHRM's controlled inputs (observed on the "To Date"
        field, which auto-populates to match "From Date" the moment the
        latter is set) don't fully empty out via a plain WebDriver
        `.clear()` - the framework's own state can retain the old value,
        so the next `send_keys` call appends instead of replacing (e.g.
        typing "2026-02-12" into a "To Date" already holding "2026-01-12"
        produced the literal, invalid string "2026-01-122026-02-12").
        Selecting all text and deleting it first forces the field to
        actually go empty before typing the new value.

        Looks for either an `<input>` or a `<textarea>` - multi-line
        fields like Claim's "Remarks" render as a `.oxd-textarea`
        `<textarea>` rather than an `<input>`, and a plain
        `By.TAG_NAME, "input"` lookup never resolves against one.
        """
        container = self._label_container(label_text, timeout)
        field = self._find_child(container, By.CSS_SELECTOR, "input, textarea", timeout)
        field.click()
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.DELETE)
        field.clear()
        field.send_keys(value)
        logger.info("Typed into '%s' field", label_text)

    def select_autocomplete_suggestion(
        self, label_text: str, query: str, timeout: Optional[int] = None
    ) -> str:
        """Types `query` into an autocomplete field (e.g. "Employee Name")
        and clicks the first *real* matching suggestion that appears,
        returning its text.

        The dropdown goes through two placeholder states that share the
        exact same `role="option"` markup as a real suggestion: a
        transient "Searching...." entry immediately after typing, then
        (if nothing matches) a "No Records Found" entry. Both must be
        explicitly excluded and waited past - grabbing "whatever
        `role='option']` appears first" reliably grabs "Searching...."
        before the real results replace it, which then fails the form's
        own "Invalid" validation once submitted.
        """
        container = self._label_container(label_text, timeout)
        field = self._find_child(container, By.TAG_NAME, "input", timeout)
        field.clear()
        field.send_keys(query)

        suggestion_locator = (By.CSS_SELECTOR, ".oxd-autocomplete-dropdown [role='option']")
        placeholder_prefixes = ("Searching", "No Records Found")

        def _real_suggestion(driver):
            for option in driver.find_elements(*suggestion_locator):
                text = option.text.strip()
                if text and not text.startswith(placeholder_prefixes):
                    return option
            return False

        try:
            suggestion = self._wait(timeout or 10).until(_real_suggestion)
        except TimeoutException as exc:
            raise ElementInteractionError(
                f"No real suggestions found for '{label_text}' with query '{query}'"
            ) from exc

        text = suggestion.text.strip()
        suggestion.click()
        logger.info(
            "Selected autocomplete suggestion '%s' for '%s' (query='%s')", text, label_text, query
        )
        return text

    def select_dropdown(self, label_text: str, option_text: str, timeout: Optional[int] = None) -> None:
        """Opens the custom `.oxd-select-text` dropdown next to the field
        labeled `label_text` and clicks the option matching `option_text`.
        """
        container = self._label_container(label_text, timeout)
        dropdown = self._find_child(container, By.CSS_SELECTOR, ".oxd-select-text", timeout)
        dropdown.click()
        option_locator = (
            By.XPATH,
            f"//div[@role='option'][.//span[normalize-space(text())='{option_text}']]",
        )
        self.click(option_locator, timeout)
        logger.info("Selected '%s' for '%s' dropdown", option_text, label_text)

    def select_first_dropdown_option(self, label_text: str, timeout: Optional[int] = None) -> str:
        """Opens the dropdown next to `label_text` and clicks the first
        real option (skipping a "-- Select --" placeholder if present).

        Used where the *set* of valid options is demo-data-dependent and
        can vary (e.g. Leave Type, Claim Event, Currency) - picking "the
        first real choice" and logging what was picked is more resilient
        than hardcoding an option name that might not exist in a given
        environment.

        Some of these dropdowns (observed on Claim's "Event") fetch their
        option list from the server *after* the dropdown opens, so the
        options panel can transiently show only a "No Records Found"
        placeholder before the real choices arrive - the exact same race
        already handled for the autocomplete suggestions below. Polling
        until a real, non-placeholder option appears avoids picking that
        placeholder as if it were a selectable choice.
        """
        container = self._label_container(label_text, timeout)
        dropdown = self._find_child(container, By.CSS_SELECTOR, ".oxd-select-text", timeout)
        dropdown.click()
        options_locator = (By.CSS_SELECTOR, "div[role='option']")
        placeholders = ("-- Select --", "No Records Found")

        def _real_options(driver):
            found = [
                o for o in driver.find_elements(*options_locator)
                if o.text.strip() and o.text.strip() not in placeholders
            ]
            return found or False

        try:
            real_options = self._wait(timeout).until(_real_options)
        except TimeoutException as exc:
            raise ElementInteractionError(
                f"No selectable options found for '{label_text}' dropdown"
            ) from exc

        option = real_options[0]
        text = option.text.strip()
        option.click()
        logger.info("Selected first available option '%s' for '%s' dropdown", text, label_text)
        return text
