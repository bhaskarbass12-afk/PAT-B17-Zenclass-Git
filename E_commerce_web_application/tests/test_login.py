"""Test-Case-1 and Test-Case-2: login with predefined users and with
invalid credentials.
"""

import pytest

from data.users import INVALID_CREDENTIALS, PREDEFINED_USERS
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


@pytest.mark.parametrize(
    "user",
    PREDEFINED_USERS,
    ids=[u["username"] for u in PREDEFINED_USERS],
)
def test_login_with_predefined_users(driver, user):
    """Test-Case-1: Login with various predefined users.

    Each user's access level and system response should behave as
    expected: locked_out_user is rejected with its specific error
    message, and every other predefined account should reach the
    products page.
    """
    login_page = LoginPage(driver).load()
    login_page.login(user["username"], user["password"])

    if user["should_succeed"]:
        products_page = ProductsPage(driver)
        assert products_page.is_displayed(), (
            f"Expected '{user['username']}' to reach the products page"
        )
    else:
        assert login_page.has_error(), (
            f"Expected '{user['username']}' to be rejected with an error"
        )
        assert user["expected_error"] in login_page.get_error_message()


@pytest.mark.parametrize(
    "credentials",
    INVALID_CREDENTIALS,
    ids=[c["username"] or "<empty-username>" for c in INVALID_CREDENTIALS],
)
def test_login_with_invalid_credentials(driver, credentials):
    """Test-Case-2: Login with invalid credentials.

    Access should be denied - an error message shown and no navigation to
    the products page - for every invalid username/password combination.
    """
    login_page = LoginPage(driver).load()
    login_page.login(credentials["username"], credentials["password"])

    assert login_page.has_error(), "Expected invalid credentials to be denied access"
    assert login_page.is_displayed(), "Expected to remain on the login page"
