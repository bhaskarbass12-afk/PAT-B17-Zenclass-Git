"""Base Page Object shared by every page in the framework.

This is the core of the framework's OOP design: every concrete page
(HomePage, LoginPage, RegisterPage) inherits explicit-wait helpers and
exception handling from here, plus a set of *header* helpers
(login/signup buttons, the logged-in avatar menu, sign-out) since GUVI's
header - and the "Login"/"Sign up"/avatar state it shows - is present on
every page in the site, not just the homepage.

A recurring, real quirk of this site's markup (confirmed by live
inspection, not assumed) is that many header elements exist *twice* in
the DOM at once - a desktop version and a mobile/responsive duplicate,
one of which is always hidden via CSS rather than removed. A locator
that just grabs "the first matching element" can silently grab the
hidden one and then fail to click it (or worse, click it "successfully"
via JS without it doing anything visible). `_first_visible` explicitly
waits for and returns whichever matching element is actually visible.
"""

from typing import Optional, Tuple

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.exceptions import ElementInteractionError, LogoutFailedError
from utils.logger import get_logger

DEFAULT_TIMEOUT = 15

Locator = Tuple[str, str]

logger = get_logger(__name__)


class BasePage:
    """Common explicit-wait, error-handling, and shared-header helpers
    for all page objects.
    """

    # -- Header locators, shared by every page on the site --------------
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Login']")
    SIGNUP_BUTTON = (By.XPATH, "//button[normalize-space()='Sign up']")
    AVATAR = (By.CSS_SELECTOR, ".gravatar-wrap")
    SIGN_OUT_OPTION = (By.XPATH, "//*[normalize-space(text())='Sign Out']")

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
        """Non-raising visibility check with a short default timeout so
        an absent element doesn't stall a test for the full page-load
        timeout.
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

    def is_any_visible(self, locator: Locator, timeout: int = 3) -> bool:
        """Non-raising visibility check that scans *every* element
        matching `locator`, not just the first DOM match.

        `is_visible` (via `EC.visibility_of_element_located`) only ever
        looks at the first element `find_element` returns for a locator.
        That's unsafe on this site: header buttons and nav items are
        each rendered twice (a desktop copy and a hidden mobile copy),
        and while the visible one happens to come first in the DOM today,
        relying on that ordering is exactly the kind of fragile
        assumption this framework avoids elsewhere (see `first_visible`).
        This checks all matches and returns True if any is displayed.
        """
        try:
            self._wait(timeout).until(
                lambda d: any(el.is_displayed() for el in d.find_elements(*locator))
            )
            return True
        except TimeoutException:
            return False

    def first_visible(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """Waits for and returns whichever element matching `locator` is
        actually visible, ignoring any hidden duplicates (this site's
        header renders a desktop *and* a mobile copy of the same button
        or nav item at once, one of which is always hidden via CSS).
        """

        def _visible_match(driver):
            for el in driver.find_elements(*locator):
                try:
                    if el.is_displayed():
                        return el
                except StaleElementReferenceException:
                    continue
            return False

        try:
            return self._wait(timeout).until(_visible_match)
        except TimeoutException as exc:
            raise ElementInteractionError(
                f"No visible element matched {locator} after {timeout or self.timeout}s"
            ) from exc

    def click_first_visible(self, locator: Locator, timeout: Optional[int] = None) -> None:
        element = self.first_visible(locator, timeout)
        try:
            element.click()
        except StaleElementReferenceException:
            self.first_visible(locator, timeout).click()

    # -- Shared header behavior ------------------------------------------

    def click_login_button(self) -> None:
        self.click_first_visible(self.LOGIN_BUTTON)
        logger.info("Clicked header 'Login' button")

    def click_signup_button(self) -> None:
        self.click_first_visible(self.SIGNUP_BUTTON)
        logger.info("Clicked header 'Sign up' button")

    def is_logged_in(self, timeout: int = 5) -> bool:
        """True if the logged-in user's avatar is visible in the header
        (the reliable signal that a session is active - the header shows
        either "Login"/"Sign up" buttons OR the avatar, never both).
        """
        return self.is_any_visible(self.AVATAR, timeout=timeout)

    def sign_out(self) -> None:
        """Opens the avatar dropdown and clicks "Sign Out". Raises
        `LogoutFailedError` if no session appears to be active, or if the
        "Login"/"Sign up" buttons don't reappear afterward.
        """
        if not self.is_logged_in():
            raise LogoutFailedError("Cannot sign out: no logged-in avatar is currently visible")

        self.click_first_visible(self.AVATAR)
        self.click_first_visible(self.SIGN_OUT_OPTION)
        logger.info("Clicked 'Sign Out'")

        if not self.is_any_visible(self.LOGIN_BUTTON, timeout=10):
            raise LogoutFailedError(
                "Clicked 'Sign Out' but the header's 'Login' button never reappeared"
            )
