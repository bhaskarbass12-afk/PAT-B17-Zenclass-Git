# import time
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumTask10:

    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def get_url(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        return f"Webpage URL is {self.url}"

    def get_title(self):
        return f"title of the page is {self.driver.title}"

    def login(self):
        self.driver.find_element(By.ID, 'user-name').send_keys("standard_user")
        self.driver.find_element(By.ID, 'password').send_keys("secret_sauce")
        self.driver.find_element(By.ID, 'login-button').click()

    def capture_text_file(self):
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        with open("Webpage_task_11.txt", "w", encoding="utf-8") as f:
            f.write(body_text)
        return "Content saved to Webpage_task_11.txt"

    def close(self):
        self.driver.quit()

Selenium_obj = SeleniumTask10(url = "https://www.saucedemo.com/")
WebpageURL= Selenium_obj.get_url()
print(WebpageURL)
Page_title= Selenium_obj.get_title()
print(Page_title)
Selenium_obj.login()
print(Selenium_obj.capture_text_file())
Selenium_obj.close()





# driver.get('https://www.saucedemo.com/')
# driver.maximize_window()
# time.sleep(2)
# driver.find_element(By.ID, 'user-name').send_keys("standard_user")
# driver.find_element(By.ID, 'password').send_keys("secret_sauce")
# driver.find_element(By.ID, 'login-button').click()
# time.sleep(2)
# driver.quit()