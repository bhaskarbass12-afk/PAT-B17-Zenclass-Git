import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Guvilogintest:

    def __init__(self, url):
        self.url = url
        headless_option = webdriver.ChromeOptions()
        headless_option.add_argument('--headless')
        headless_option.add_argument('--window-size=1920,1080')  # Forces desktop layout
        headless_option.add_argument('--disable-gpu')  # Recommended for Windows headless
        headless_option.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=headless_option)
        self.wait = WebDriverWait(self.driver, 10)



    def get_url(self):
        self.driver.get(self.url)
        self.wait.until(EC.title_contains("GUVI"))
        print("Webpage is opened successfully")
        return f"Webpage Url is {self.url}"

    def get_tittle(self):
        return f"Title of the page is {self.driver.title}"

    def login(self):
        self.driver.get("https://www.guvi.in/")

        main_login = self.wait.until(EC.visibility_of_element_located((By.XPATH, "(//button[contains(text(),'Login')])[1]")))
        main_login.click()


        #Wait for the email field to be visible before interacting
        email_field = self.wait.until(EC.visibility_of_element_located((By.ID, "email")))
        email_field.send_keys("bhaskarbass12@gmail.com")

        #Wait for password field
        password_field = self.wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_field.send_keys("Bhaskar@2703")

        # Wait for login button to be clickable
        login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='login-btn']")))
        login_btn.click()

        # Optional: wait for navigation after login (adjust locator to something on the dashboard)
        # self.wait.until(EC.url_contains("/courses"))

    def close_browser(self):
        self.driver.quit()

Guvilogintest_obj = Guvilogintest(url = "https://www.guvi.in/")
print(Guvilogintest_obj.get_url())
print(Guvilogintest_obj.get_tittle())
Guvilogintest_obj.login()
Guvilogintest_obj.close_browser()



