from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.ie.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

class GuviHome:
    driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def __init__(self, url):
        self.url = url

    def visit_url(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def open_signup_page(self):
        self.driver.find_element(By.ID, 'login-btn').click()
        time.sleep(2)
        self.driver.back()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[text()='Sign up']").click()
        time.sleep(2)
        self.driver.back()

    def close(self):
        self.driver.close()

GuviHomeAuto = GuviHome("https://www.guvi.in/")
GuviHomeAuto.visit_url()
GuviHomeAuto.open_signup_page()
GuviHomeAuto.close()







