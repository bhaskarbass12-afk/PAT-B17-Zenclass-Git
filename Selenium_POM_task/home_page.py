from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Base_page import BasePage

class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.profile_menu = (By.XPATH, "//p[contains(@class, 'avatar-profile-name')]")
        self.logout_btn = (By.XPATH, "//div[@class='user-avatar-menu' and contains(text(), 'Log out')]")
        self.pop_cancel = (By.XPATH, "//button[@class='custom-close-button']")

    def is_logged_in(self):
        """Logged in when the profile menu is visible."""
        try:
            return self.wait.until(
                ec.visibility_of_element_located(self.profile_menu)
            ).is_displayed()
        except TimeoutException:
            return False

    def logout(self):
        # close any welcome pop-up if present (don't fail if it isn't there)
        try:
            self.wait.until(ec.element_to_be_clickable(self.pop_cancel)).click()
        except TimeoutException:
            pass
        self.wait.until(ec.element_to_be_clickable(self.profile_menu)).click()
        self.wait.until(ec.element_to_be_clickable(self.logout_btn)).click()

    def is_logout_successful(self):
        login_marker = (By.XPATH, "//input[@placeholder='Enter your mail']")
        try:
            return self.wait.until(
                ec.visibility_of_element_located(login_marker)
            ).is_displayed()
        except TimeoutException:
            return False
