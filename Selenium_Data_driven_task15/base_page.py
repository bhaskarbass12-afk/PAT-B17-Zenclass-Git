from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class BasePage:
    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        if driver is None:
            raise ValueError("A valid WebDriver instance is required.")
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    @staticmethod
    def invoke_browser():
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(options=options)
        return driver
