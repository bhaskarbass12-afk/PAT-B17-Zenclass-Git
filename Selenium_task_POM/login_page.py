from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)          # sets self.driver and self.wait
        self.email = (By.XPATH, "//input[@placeholder='Enter your mail']")
        self.password = (By.XPATH, "//input[@placeholder='Enter your password ']")
        self.signin = (By.XPATH, "//button[@type='submit']")
        self.remember = (By.CLASS_NAME, "remeber-me-text")
        self.forgot_pwd = (By.CLASS_NAME, "forgot-text-container")
        self.incorrect = (By.XPATH, "//p[contains(@class, 'MuiFormHelperText-filled')]")


    def open_url(self):
        self.driver.get("https://v2.zenclass.in/login")

    def login(self):
        self.wait.until(EC.visibility_of_element_located(self.email)).send_keys("bhaskarbass12@gmail.com")
        self.wait.until(EC.visibility_of_element_located(self.password)).send_keys("Bhaskar@2703")
        self.wait.until(EC.visibility_of_element_located(self.signin)).click()

    def check_for_unsuccessful_login(self):
        try:
            # wait up to 15s for the error message to appear
            return self.wait.until(
                EC.visibility_of_element_located(self.incorrect)
            ).is_displayed()
        except TimeoutException:
            return False

    def forgot_password(self):
        self.driver.find_element(self.forgot_pwd).click()


if __name__ == "__main__":
    driver = BasePage.invoke_browser()      # create the driver
    login = LoginPage(driver)               # object definition here
    login.open_url()
    login.login()

    if login.check_for_unsuccessful_login():
        print("Login failed as expected")
    else:
        print("Login succeeded")

    driver.quit()