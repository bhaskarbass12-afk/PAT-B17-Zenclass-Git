import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Actionchain:

    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(service=Service((ChromeDriverManager().install())))
        self.wait = WebDriverWait(self.driver, 10)

    def get_url(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(3)
        print(f"Webpage opened successfully: {self.url}")
        return self.driver.current_url

    def get_title(self):
        title = self.driver.title
        print(f"Title of the page is {title}")
        return title

    def switch_to_frame(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME , 'demo-frame')))
        self.driver.switch_to.frame(iframe)
        print("Switched to iframe successfully")

    def perform_drag_drop(self):
        self.switch_to_frame()
        source = self.wait.until(EC.visibility_of_element_located((By.ID, 'draggable')))
        target = self.wait.until(EC.visibility_of_element_located((By.ID, 'droppable')))

        # Perform drag and drop using ActionChains
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source, target).perform()
        time.sleep(2)
        print("Drag and Drop action performed successfully")

        # Return the droppable box text so tests can assert on it
        return target.text

    def perform_invalid_drop(self):
        """Negative scenario: nudge the draggable without landing on the target."""
        self.switch_to_frame()
        source = self.wait.until(EC.visibility_of_element_located((By.ID, 'draggable')))
        target = self.wait.until(EC.visibility_of_element_located((By.ID, 'droppable')))

        # Only move a small offset, never over the yellow box
        actions = ActionChains(self.driver)
        actions.click_and_hold(source).move_by_offset(10, 10).release().perform()
        time.sleep(2)
        print("Invalid (incomplete) drag action performed")
        return target.text

    def quit(self):
        self.driver.quit()

if __name__ == "__main__":
    Actionchain_obj = Actionchain(url="https://jqueryui.com/droppable/")
    Actionchain_obj.get_url()
    Actionchain_obj.get_title()
    Actionchain_obj.perform_drag_drop()
    Actionchain_obj.quit()





