from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.exceptions import LoginFailedError


class LoginPage(BasePage):
    """Encapsulates all locators and actions for the login screen."""

    URL = "https://www.saucedemo.com/"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def load(self) -> "LoginPage":
        """Navigates to the login page and explicitly waits for it to render."""
        self.driver.get(self.URL)
        self.find(self.USERNAME_INPUT)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """Full login flow: fill username, password, and submit."""
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def is_displayed(self) -> bool:
        return self.is_visible(self.USERNAME_INPUT)

    def has_error(self) -> bool:
        """Explicit wait for the error banner; returns False on timeout
        instead of raising, since "no error" is a valid outcome too.
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=5)

    def get_error_message(self) -> str:
        if not self.has_error():
            raise LoginFailedError(
                "Expected a login error message to be displayed, but none was found"
            )
        return self.get_text(self.ERROR_MESSAGE)