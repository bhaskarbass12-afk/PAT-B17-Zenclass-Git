"""Page Object for the GUVI sign-in page (https://www.guvi.in/sign-in/)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Encapsulates the "Or Login with Email" form on the sign-in page.

    Note: the site also offers a "Sign in with Google" button, but that
    flow requires interactive Google account consent and can't be
    driven headlessly with a real account - this framework only
    automates the email/password form, which the brief's test cases
    describe.
    """

    URL = "https://www.guvi.in/sign-in/"
    URL_FRAGMENT = "sign-in"

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_SUBMIT = (By.ID, "login-btn")
    # Confirmed via live inspection: this site renders the same
    # "Incorrect Email or Password" message twice (once under the email
    # field, once under the password field) when login fails - both
    # share the `.invalid-feedback` class.
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".invalid-feedback")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def load(self) -> "LoginPage":
        self.driver.get(self.URL)
        logger.info("Loaded login page: %s", self.URL)
        return self

    def is_displayed(self) -> bool:
        return self.wait_until_url_contains(self.URL_FRAGMENT)

    def login(self, email: str, password: str) -> None:
        """Fills in and submits the email/password login form. Does not
        assert on the outcome - callers check `is_logged_in()` (success)
        or `get_error_message()` (failure) afterward, since either is a
        valid, expected outcome depending on the test case.
        """
        email_field = self.find(self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)

        password_field = self.find(self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)

        self.click(self.LOGIN_SUBMIT)
        logger.info("Submitted login form for '%s'", email)

    def get_error_message(self) -> str:
        return self.first_visible(self.ERROR_MESSAGE).text
