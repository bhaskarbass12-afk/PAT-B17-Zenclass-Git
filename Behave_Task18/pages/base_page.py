"""Base Page Object shared by every page in the Zen Portal BDD test suite."""

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 15


class BasePage:
    """Common explicit-wait helpers, inherited by every concrete Page Object.

    Demonstrates OOP: encapsulates the WebDriver handle and timeout policy,
    and is subclassed (inheritance) by LoginPage and DashboardPage.
    """

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, timeout: int = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.timeout)

    def wait_for_visible(self, locator, timeout: int = None) -> WebElement:
        """Explicit wait: block until the element at `locator` is visible."""
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator, timeout: int = None) -> WebElement:
        """Explicit wait: block until the element at `locator` is clickable."""
        return self._wait(timeout).until(EC.element_to_be_clickable(locator))

    def is_visible_within_timeout(self, locator, timeout: int = None) -> bool:
        """Explicit wait that swallows TimeoutException / NoSuchElementException
        and returns False instead of raising. Useful for optional/conditional
        UI elements (popups, error banners) that may or may not appear. Pass
        a shorter `timeout` for "is this already here?" checks so absent
        elements don't stall the scenario for the full default timeout.
        """
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_url_contains(self, fragment: str, timeout: int = None) -> bool:
        """Explicit wait until the current URL contains `fragment`."""
        try:
            return self._wait(timeout).until(EC.url_contains(fragment))
        except TimeoutException:
            return False

    def safe_click(self, locator, timeout: int = None) -> None:
        """Click an element, retrying once if another element intercepts the
        click (common with closing overlays/popups) or the element goes
        stale between locating and clicking.
        """
        element = self.wait_for_clickable(locator, timeout)
        try:
            element.click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            element = self.wait_for_clickable(locator, timeout)
            element.click()