import pytest
from Base_page import BasePage
from login_page import LoginPage
from home_page import HomePage

@pytest.fixture
def driver():
    """Fresh browser per test, quit afterwards."""
    drv = BasePage.invoke_browser()
    yield drv
    drv.quit()

@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    page.open_url()
    return page

@pytest.fixture
def logged_in_home(login_page):
    """Log in with valid creds and hand back the HomePage."""
    login_page.login()  # valid credentials
    home = HomePage(login_page.driver)
    assert home.is_logged_in(), "Setup failed: could not log in with valid credentials."
    return home
