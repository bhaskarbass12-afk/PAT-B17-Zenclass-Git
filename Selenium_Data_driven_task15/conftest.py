import pytest
from base_page import BasePage
from login_page import LoginPage
from excel_utils import ExcelManager

@pytest.fixture(scope="session")
def excel():
    return ExcelManager()

@pytest.fixture
def login_page():
    driver = BasePage.invoke_browser()
    page = LoginPage(driver)
    page.open()
    yield page
    driver.quit()
