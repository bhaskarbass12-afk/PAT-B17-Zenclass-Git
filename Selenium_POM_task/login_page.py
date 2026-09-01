from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from Base_page import BasePage

class LoginPage(BasePage):

    URL = "https://v2.zenclass.in/login"

    # ---- valid credentials (change to your own) ----
    VALID_EMAIL = "bhaskarbass12@gmail.com"
    VALID_PASSWORD = "Bhaskar@2703"

    def __init__(self, driver):
        super().__init__(driver)
        self.email = (By.XPATH, "//input[@placeholder='Enter your mail']")
        self.password = (By.XPATH, "//input[@placeholder='Enter your password ']")
        self.signin = (By.XPATH, "//button[@type='submit']")
        self.remember = (By.CLASS_NAME, "remeber-me-text")
        self.forgot_pwd = (By.CLASS_NAME, "forgot-text-container")
        self.incorrect = (By.XPATH, "//p[contains(@class, 'MuiFormHelperText-filled')]")

    def open_url(self):
        self.driver.get(self.URL)

    def login(self, email=None, password=None):
        """Log in. Uses valid creds by default, or the given values."""
        email = self.VALID_EMAIL if email is None else email
        password = self.VALID_PASSWORD if password is None else password

        email_box = self.wait.until(EC.visibility_of_element_located(self.email))
        email_box.clear()
        email_box.send_keys(email)

        pwd_box = self.wait.until(EC.visibility_of_element_located(self.password))
        pwd_box.clear()
        pwd_box.send_keys(password)

        self.wait.until(EC.element_to_be_clickable(self.signin)).click()

    def check_for_unsuccessful_login(self):
        """True if the inline error message is shown."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.incorrect)
            ).is_displayed()
        except TimeoutException:
            return False

    # ---------- helpers used by the pytest validations ----------

    def is_email_input_displayed(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.email)
            ).is_displayed()
        except TimeoutException:
            return False

    def is_password_input_displayed(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.password)
            ).is_displayed()
        except TimeoutException:
            return False

    def type_email(self, value):
        box = self.wait.until(EC.visibility_of_element_located(self.email))
        box.clear()
        box.send_keys(value)
        return box.get_attribute("value")

    def type_password(self, value):
        box = self.wait.until(EC.visibility_of_element_located(self.password))
        box.clear()
        box.send_keys(value)
        return box.get_attribute("value")

    def is_submit_enabled(self):
        try:
            btn = self.wait.until(EC.presence_of_element_located(self.signin))
            return btn.is_enabled()
        except TimeoutException:
            return False

    def click_submit(self):
        self.wait.until(EC.element_to_be_clickable(self.signin)).click()

    def is_on_login_page(self):
        return "login" in self.driver.current_url.lower()

    def forgot_password(self):
        try:
            self.driver.find_element(*self.forgot_pwd).click()
        except NoSuchElementException:
            raise NoSuchElementException("Forgot-password link not found.")
