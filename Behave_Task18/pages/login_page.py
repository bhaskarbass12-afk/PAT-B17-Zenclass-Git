"""Page Object for the Zen Portal login page (https://v2.zenclass.in/login)."""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates all locators and actions for the login screen."""

    URL = "https://v2.zenclass.in/login"

    EMAIL_INPUT = (By.CSS_SELECTOR, "input[placeholder='Enter your mail']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder^='Enter your password']")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Sign in']")
    ERROR_MESSAGE = (By.XPATH, "//*[contains(text(), 'Invalid email')]")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def load(self) -> "LoginPage":
        """Navigate to the login page and explicitly wait for it to render."""
        self.driver.get(self.URL)
        self.wait_for_visible(self.EMAIL_INPUT)
        return self

    def enter_email(self, email: str) -> "LoginPage":
        field = self.wait_for_visible(self.EMAIL_INPUT)
        field.clear()
        field.send_keys(email)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        field = self.wait_for_visible(self.PASSWORD_INPUT)
        field.clear()
        field.send_keys(password)
        return self

    def click_sign_in(self) -> "LoginPage":
        self.safe_click(self.SUBMIT_BUTTON)
        return self

    def login(self, email: str, password: str) -> "LoginPage":
        """Full login flow: fill email, password, and submit."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_sign_in()
        return self

    def get_email_value(self) -> str:
        return self.wait_for_visible(self.EMAIL_INPUT).get_attribute("value")

    def get_password_value(self) -> str:
        return self.wait_for_visible(self.PASSWORD_INPUT).get_attribute("value")

    def get_password_field_type(self) -> str:
        return self.wait_for_visible(self.PASSWORD_INPUT).get_attribute("type")

    def is_submit_button_visible(self) -> bool:
        return self.is_visible_within_timeout(self.SUBMIT_BUTTON)

    def is_submit_button_enabled(self) -> bool:
        try:
            return self.wait_for_visible(self.SUBMIT_BUTTON).is_enabled()
        except NoSuchElementException:
            return False

    def is_email_input_visible(self) -> bool:
        return self.is_visible_within_timeout(self.EMAIL_INPUT)

    def is_error_displayed(self) -> bool:
        """Explicit wait for the credential-error banner; returns False on timeout."""
        return self.is_visible_within_timeout(self.ERROR_MESSAGE)

    def get_error_text(self) -> str:
        return self.wait_for_visible(self.ERROR_MESSAGE).text

    def wait_for_url_fragment(self, fragment: str) -> bool:
        return self.wait_for_url_contains(fragment)