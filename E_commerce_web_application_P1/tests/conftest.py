import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from data.users import PASSWORD
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


@pytest.fixture
def driver():
    options = Options()
    if os.getenv("HEADLESS", "true").lower() != "false":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    drv = webdriver.Chrome(options=options)
    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture
def logged_in_products_page(driver) -> ProductsPage:
    """A ProductsPage for an already-logged-in 'standard_user' session.

    Used by tests whose scenario starts *after* login (cart, sorting,
    reset, checkout) so they don't each have to re-implement the login
    steps, while still getting a fresh browser/session per test.
    """
    LoginPage(driver).load().login("standard_user", PASSWORD)
    page = ProductsPage(driver)
    assert page.is_displayed(), "Expected standard_user login to land on the products page"
    return page
