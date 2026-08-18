import pytest
import time
from Guvi_headlessbrowser import Guvilogintest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="class")
def setup(request):
    """Create Guvilogintest instance and share driver with test class."""
    obj = Guvilogintest(url="https://www.guvi.in/sign-in/")
    request.cls.obj = obj
    request.cls.driver = obj.driver
    request.cls.wait = WebDriverWait(obj.driver, 15)
    yield
    obj.close_browser()


@pytest.mark.usefixtures("setup")
class TestGuviLoginPage:

    # ========================
    # POSITIVE TEST CASES
    # ========================

    def test_positive_login_url(self):
        """TC01 - Validate that the login page URL is https://www.guvi.in/sign-in/"""
        self.driver.get("https://www.guvi.in/sign-in/")
        self.wait.until(EC.url_contains("sign-in"))
        assert "sign-in" in self.driver.current_url

    def test_positive_username_visible_and_enabled(self):
        """TC02 - Validate that the Username input box is visible and enabled."""
        self.driver.get("https://www.guvi.in/sign-in/")
        email_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        assert email_field.is_displayed()
        assert email_field.is_enabled()

    def test_positive_password_visible_and_enabled(self):
        """TC03 - Validate that the Password input box is visible and enabled."""
        self.driver.get("https://www.guvi.in/sign-in/")
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        assert password_field.is_displayed()
        assert password_field.is_enabled()

    def test_positive_submit_button_clickable(self):
        """TC04 - Validate that the Submit button is working properly."""
        self.driver.get("https://www.guvi.in/sign-in/")
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "login-btn"))
        )
        assert login_btn.is_displayed()
        assert login_btn.is_enabled()

    def test_positive_login_with_valid_credentials(self):
        """TC05 - Validate login with valid credentials."""
        self.obj.login()
        time.sleep(5)
        assert self.driver.current_url is not None

    # ========================
    # NEGATIVE TEST CASES
    # ========================

    def test_negative_invalid_url(self):
        """TC06 - Validate that an invalid URL does not show sign-in form."""
        self.driver.get("https://www.guvi.in/invalid-page/")
        time.sleep(3)
        elements = self.driver.find_elements(By.ID, "email")
        assert len(elements) == 0

    def test_negative_empty_username(self):
        """TC07 - Validate that empty username prevents login."""
        self.driver.get("https://www.guvi.in/sign-in/")
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys("SomePassword@123")
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "login-btn"))
        )
        login_btn.click()
        time.sleep(3)
        assert "sign-in" in self.driver.current_url

    def test_negative_empty_password(self):
        """TC08 - Validate that empty password prevents login."""
        self.driver.get("https://www.guvi.in/sign-in/")
        email_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        email_field.clear()
        email_field.send_keys("bhaskarbass12@gmail.com")
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "login-btn"))
        )
        login_btn.click()
        time.sleep(3)
        assert "sign-in" in self.driver.current_url

    def test_negative_invalid_credentials(self):
        """TC09 - Validate that invalid credentials are rejected."""
        self.driver.get("https://www.guvi.in/sign-in/")
        email_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        email_field.clear()
        email_field.send_keys("fake_user@invalid.com")
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys("WrongPass@999")
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "login-btn"))
        )
        login_btn.click()
        time.sleep(5)
        assert "sign-in" in self.driver.current_url

    def test_negative_submit_without_any_input(self):
        """TC10 - Validate that clicking submit with no input stays on sign-in."""
        self.driver.get("https://www.guvi.in/sign-in/")
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "login-btn"))
        )
        login_btn.click()
        time.sleep(3)
        assert "sign-in" in self.driver.current_url