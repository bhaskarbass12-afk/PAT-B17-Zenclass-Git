import pytest
from selenium.webdriver.common.by import By

from Selenium_Day1 import SeleniumTask10
import time

url = "https://www.saucedemo.com/"


class TestSeleniumPytest:

    def setup_method(self):
        self.selenium = SeleniumTask10(url)
        self.selenium.get_url()

    def teardown_method(self):
        self.selenium.close()

    def test_positive_url(self):
        expected = f"Webpage URL is {url}"
        actual = self.selenium.get_url()
        assert actual == expected
        print("SUCCESS: Test Positive URL Passed")

    def test_negative_url(self):
        wrong_url = "http://www.saucedemo.com/"
        expected = f"Webpage URL is {wrong_url}"
        actual = self.selenium.get_url()
        assert actual != expected
        print("SUCCESS: Test Negative URL Passed")

    def test_positive_title(self):
        expected = "title of the page is Swag Labs"
        actual = self.selenium.get_title()
        assert actual == expected
        print("SUCCESS: Test Positive Title Passed")

    def test_negative_title(self):
        expected = "title of the page is Swag Labss"
        actual = self.selenium.get_title()
        assert actual != expected
        print("SUCCESS: Test Negative Title Passed")

    def test_positive_login(self):
        """Test login with valid credentials - should redirect to inventory page"""
        self.selenium.driver.find_element(By.ID, 'user-name').send_keys("standard_user")
        self.selenium.driver.find_element(By.ID, 'password').send_keys("secret_sauce")
        self.selenium.driver.find_element(By.ID, 'login-button').click()
        time.sleep(2)
        current_url = self.selenium.driver.current_url
        assert "inventory" in current_url
        print("SUCCESS: Test Positive Login Passed")

    def test_negative_login_wrong_password(self):
        """Test login with invalid password - should show error message"""
        self.selenium.driver.find_element(By.ID, 'user-name').send_keys("standard_user")
        self.selenium.driver.find_element(By.ID, 'password').send_keys("wrong_password")
        self.selenium.driver.find_element(By.ID, 'login-button').click()
        time.sleep(2)
        error_message = self.selenium.driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
        assert error_message.is_displayed()
        assert "Username and password do not match" in error_message.text
        print("SUCCESS: Test Negative Login (Wrong Password) Passed")

    def test_negative_login_wrong_username(self):
        """Test login with invalid username - should show error message"""
        self.selenium.driver.find_element(By.ID, 'user-name').send_keys("invalid_user")
        self.selenium.driver.find_element(By.ID, 'password').send_keys("secret_sauce")
        self.selenium.driver.find_element(By.ID, 'login-button').click()
        time.sleep(2)
        error_message = self.selenium.driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
        assert error_message.is_displayed()
        assert "Username and password do not match" in error_message.text
        print("SUCCESS: Test Negative Login (Wrong Username) Passed")

    def test_negative_login_empty_fields(self):
        """Test login with empty credentials - should show error message"""
        self.selenium.driver.find_element(By.ID, 'login-button').click()
        time.sleep(2)
        error_message = self.selenium.driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
        assert error_message.is_displayed()
        assert "Username is required" in error_message.text
        print("SUCCESS: Test Negative Login (Empty Fields) Passed")

    def test_negative_login_locked_user(self):
        """Test login with locked out user - should show locked out error"""
        self.selenium.driver.find_element(By.ID, 'user-name').send_keys("locked_out_user")
        self.selenium.driver.find_element(By.ID, 'password').send_keys("secret_sauce")
        self.selenium.driver.find_element(By.ID, 'login-button').click()
        time.sleep(2)
        error_message = self.selenium.driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
        assert error_message.is_displayed()
        assert "this user has been locked out" in error_message.text
        print("SUCCESS: Test Negative Login (Locked User) Passed")