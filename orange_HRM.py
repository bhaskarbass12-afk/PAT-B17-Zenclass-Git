import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
driver.maximize_window()
time.sleep(5)
driver.find_element(By.XPATH,"//input[@name='username']").send_keys("Admin")
driver.find_element(By.XPATH, "//input[@name='password']").send_keys("admin123")
driver.find_element(By.XPATH, "//button[@class='oxd-button oxd-button--medium oxd-button--main orangehrm-login-button']").click()
time.sleep(5)
driver.find_element(By.XPATH, "//span[@class='oxd-text oxd-text--span oxd-main-menu-item--name']").click()
time.sleep(5)
driver.find_element(By.XPATH, "//button[@class='oxd-button oxd-button--medium oxd-button--secondary']").click()
# user = driver.find_elements(By.XPATH, "//div[@role='listbox']")
# time.sleep(5)
# for user_element in user:
#     if options == user_element:
#         driver.find_element(By.XPATH, "//div[@class='oxd-select-option'][2]").click()
#         break
#     elif options == user_element:
#         driver.find_element(By.XPATH, "//div[@class='oxd-select-option'][3]").click()
#         break
#     else:
#         continue


