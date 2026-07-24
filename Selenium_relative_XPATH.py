import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.guvi.in/")
time.sleep(2)
print (driver.find_element(By.XPATH, "//div[3]/div/div/p[text()='LIVE Classes']").text)
print (driver.find_element(By.XPATH, "//header/div/div[3]/div[3]/div/p").text)
print (driver.find_element(By.XPATH, "//div[4]/div[@id='solutions']/p").text)
print (driver.find_element(By.XPATH, "//div[5]/div[@id='solutions']/p").text)
login = driver.find_element(By.XPATH, "//div[4]/div/button[@id='login-btn']").text
print(login)
print (driver.find_element(By.XPATH, "//div[4]/div/button[text()='Sign up']").text)





# Absolute Xpath for the "Course" in the Guvi website
# Course Absolute XPath = "/html/body/main/header/div/div[3]/div[2]/div/p"
# Course Relative XPath = "//div[3]/div[2]/div/p"
# Parent for Course Relative Xpath = //div[3]/div[2]/div/p/parent::div[@id='solutions']
# child for Course Relative Xpath = //div[3]/div[2]/div/p/parent::*/child::*[1]
# ancestor for course = //div[3]/div[2]/div/p/ancestor::div[2]
#Parentelement with href = //div[3]/div/div/p[text()='LIVE Classes']/ancestor::*/div/div/div[2]/a

# Live courses
#Relative XPATH = //div[3]/div/div/p[text()='LIVE Classes']
#Parent = //div[3]/div/div/p[text()='LIVE Classes']/parent::div[@id='solutions']
#ancestor = //div[3]/div/div/p[text()='LIVE Classes']/ancestor::div
#sibiling = //div[3]/div[1]/div[@id='solutions']/following-sibling::div[1]
#sibiling = //header/div/div[3]/div[1]/child::div[2]/preceding-sibling::div

#Practice

#XPATH = //header/div/div[3]/div[3]/div/p
#Parent = //header/div/div[3]/div[3]/div[@id='solutions']
#ancestor= //div[3]/div[3]/div[@id='solutions']/ancestor::div[1]2

#resource

#XPATH = //div[4]/div[@id='solutions']/p
#parent = //div[4]/div[@id='solutions']
#ancestor = //div[4]/div[@id='solutions']/ancestor::div[3]
#sibilings = //div[4]/div[@id='solutions']/following-sibling::div

#our products

#XPATH = //div[5]/div[@id='solutions']/p
#parent = //div[5]/div[@id='solutions']
#ancestor = //div[5]/div[@id='solutions']/ancestor::div[1]'
#sibilings = //div[5]/div[@id='solutions']/following-sibling::div


#Login

#XPATH = //div[4]/div/button[@id="login-btn"]
#parent = //div[4]/div/button[@id="login-btn"]/parent::div
#ancestor = //div[4]/div/button[@id="login-btn"]/ancestor::div[2]
#sibilings = //div[4]/div/button[@id="login-btn"]/following-sibling::button

#Sign up

#XPATH = //div[4]/div/button[text()="Sign up"]
#parent = //div[4]/div/button[text()="Sign up"]/parent::div
#ancestor = //div[4]/div/button[text()="Sign up"]/ancestor::div[2]
#sibilings = //div[4]/div/button[text()="Sign up"]/preceding-sibling::button
