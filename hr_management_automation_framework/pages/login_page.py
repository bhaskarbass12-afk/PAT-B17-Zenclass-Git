"""Page Object for the OrangeHRM login page."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.exceptions import LoginFailedError
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Encapsulates all locators and actions for the login screen."""

    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    # Wrong-but-non-empty credentials show the top-level alert banner
    # (server-side rejection). Leaving a field blank instead triggers
    # client-side "Required" validation under that specific field, which
    # never reaches the server and never shows the alert banner - so both
    # must be checked to cover every invalid-credentials scenario.
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".oxd-alert-content--error")
    FIELD_ERROR_MESSAGE = (By.CSS_SELECTOR, ".oxd-input-field-error-message")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//p[contains(@class,'orangehrm-login-forgot-header')]")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def load(self) -> "LoginPage":
        """Navigates to the login page and explicitly waits for it to render."""
        self.driver.get(self.URL)
        self.find(self.USERNAME_INPUT)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """Full login flow: fill username, password, and submit."""
        username_field = self.find(self.USERNAME_INPUT)
        username_field.clear()
        username_field.send_keys(username)

        password_field = self.find(self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)

        self.click(self.LOGIN_BUTTON)
        logger.info("Submitted login form for user '%s'", username or "<empty>")
        return self

    def is_displayed(self) -> bool:
        return self.is_visible(self.USERNAME_INPUT)

    def has_error(self) -> bool:
        """Explicit wait for either the top-level error banner (wrong
        credentials) or a field-level "Required" validation message
        (an empty field); returns False on timeout instead of raising,
        since "no error" is a valid outcome too.
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=5) or self.is_visible(
            self.FIELD_ERROR_MESSAGE, timeout=2
        )

    def get_error_message(self) -> str:
        if self.is_visible(self.ERROR_MESSAGE, timeout=2):
            return self.get_text(self.ERROR_MESSAGE)
        if self.is_visible(self.FIELD_ERROR_MESSAGE, timeout=2):
            return self.get_text(self.FIELD_ERROR_MESSAGE)
        raise LoginFailedError(
            "Expected a login error message to be displayed, but none was found"
        )

    def click_forgot_password(self) -> None:
        self.click(self.FORGOT_PASSWORD_LINK)
