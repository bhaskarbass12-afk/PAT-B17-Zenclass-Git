from playwright.sync_api import Page

from base_page import BasePage


class LoginPage(BasePage):

    URL = "https://v2.zenclass.in/login"

    def __init__(self, page: Page, timeout: int = 15000):
        super().__init__(page, timeout)
        self.email_input = page.get_by_placeholder("Enter your mail")
        self.password_input = page.get_by_placeholder("Enter your password")
        self.submit_button = page.get_by_role("button", name="Sign in")
        self.error_message = page.get_by_text("Invalid email!")

    def load(self) -> "LoginPage":
        self.page.goto(self.URL, wait_until="networkidle", timeout=self.timeout)
        self.wait_for_visible(self.email_input)
        return self

    def enter_email(self, email: str) -> "LoginPage":
        self.wait_for_visible(self.email_input)
        self.email_input.fill(email)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.wait_for_visible(self.password_input)
        self.password_input.fill(password)
        return self

    def click_sign_in(self) -> "LoginPage":
        self.wait_for_visible(self.submit_button)
        self.submit_button.click()
        return self

    def login(self, email: str, password: str) -> "LoginPage":
        self.enter_email(email)
        self.enter_password(password)
        self.click_sign_in()
        return self

    def is_submit_button_enabled(self) -> bool:
        return self.submit_button.is_enabled()

    def is_error_displayed(self) -> bool:
        return self.is_visible_within_timeout(self.error_message)

    def get_error_text(self) -> str:
        self.wait_for_visible(self.error_message)
        return self.error_message.inner_text()