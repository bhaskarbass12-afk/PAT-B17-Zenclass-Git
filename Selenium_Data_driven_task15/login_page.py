from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base_page import BasePage

class LoginPage(BasePage):

    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    def __init__(self, driver):
        super().__init__(driver)
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.dashboard_header = (By.XPATH, "//h6[text()='Dashboard']")
        self.error_alert = (By.XPATH, "//div[@role='alert']//p")
        self.required_field = (By.XPATH, "//span[text()='Required']")

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.username_input))

    def login(self, username, password):
        """Enter credentials, submit, and return True if login succeeded."""
        user_box = self.wait.until(EC.visibility_of_element_located(self.username_input))
        user_box.clear()
        user_box.send_keys(username)

        pwd_box = self.wait.until(EC.visibility_of_element_located(self.password_input))
        pwd_box.clear()
        pwd_box.send_keys(password)

        self.wait.until(EC.element_to_be_clickable(self.login_button)).click()

        return self._is_login_successful()

    def _is_login_successful(self):
        """True if the dashboard shows up; False if an error/required msg appears."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.dashboard_header))
            return True
        except TimeoutException:
            return False
