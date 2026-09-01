from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Base_page import BasePage
from login_page import LoginPage


class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.profile_menu = (By.XPATH, "//p[contains(@class, 'avatar-profile-name')]")
        self.logout_btn = (By.XPATH, "//div[@class='user-avatar-menu' and contains(text(), 'Log out')]")
        self.pop_cancel = (By.XPATH, "//button[@class='custom-close-button']")

    def logout(self):
        # if logout is behind a menu, open it first
        self.wait.until(ec.element_to_be_clickable(self.pop_cancel)).click()
        self.wait.until(ec.element_to_be_clickable(self.profile_menu)).click()
        self.wait.until(ec.element_to_be_clickable(self.logout_btn)).click()

    def is_logout_successful(self):
        # back on the login screen means logout worked
        login_marker = (By.XPATH, "//input[@placeholder='Enter your mail']")
        try:
            return self.wait.until(
                ec.visibility_of_element_located(login_marker)
            ).is_displayed()
        except TimeoutException:
            return False

if __name__ == "__main__":
    driver = BasePage.invoke_browser()

    login = LoginPage(driver)
    login.open_url()
    login.login()

    home = HomePage(driver)
    home.logout()

    if home.is_logout_successful():
        print("Logout successful")
    else:
        print("Logout failed")

    driver.quit()