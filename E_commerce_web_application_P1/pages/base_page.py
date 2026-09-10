from typing import List, Optional, Tuple

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.exceptions import ElementInteractionError

DEFAULT_TIMEOUT = 15

Locator = Tuple[str, str]


class BasePage:
    """Common explicit-wait and error-handling helpers for all page objects."""

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.timeout)

    def find(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """Explicit wait for `locator` to be visible, raising a clear,
        framework-specific error instead of a raw Selenium traceback if it
        never appears.
        """
        try:
            return self._wait(timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException as exc:
            raise ElementInteractionError(
                f"Element {locator} was not visible after {timeout or self.timeout}s"
            ) from exc

    def find_all(self, locator: Locator, timeout: Optional[int] = None) -> List[WebElement]:
        """Explicit wait for at least one match of `locator`, then returns
        every element currently matching it.
        """
        try:
            self._wait(timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException as exc:
            raise ElementInteractionError(
                f"No elements matched {locator} after {timeout or self.timeout}s"
            ) from exc
        return self.driver.find_elements(*locator)

    def click(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """Clicks an element, retrying once if it goes stale between being
        located and clicked - a real, occasionally-observed flakiness
        source on dynamic pages.
        """
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

    def type_text(self, locator: Locator, text: str, timeout: Optional[int] = None) -> None:
        field = self.find(locator, timeout)
        field.clear()
        field.send_keys(text)

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        return self.find(locator, timeout).text

    def is_visible(self, locator: Locator, timeout: int = 3) -> bool:
        """Non-raising visibility check for optional/conditional elements.
        Uses a short default timeout so an absent element doesn't stall a
        test for the full page-load timeout.
        """
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_until_url_contains(self, fragment: str, timeout: Optional[int] = None) -> bool:
        try:
            return bool(self._wait(timeout).until(EC.url_contains(fragment)))
        except TimeoutException:
            return False