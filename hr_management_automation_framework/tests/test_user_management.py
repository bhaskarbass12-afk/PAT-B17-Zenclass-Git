"""Test-Case-5 and Test-Case-6: creating a new user and validating both
that it can log in, and that it appears in the admin user list.
"""

import time

from data.users import EXISTING_EMPLOYEE_SEARCH_TEXT
from pages.admin_user_page import AdminUserListPage
from pages.authenticated_page import AuthenticatedPage
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)

NEW_USER_PASSWORD = "Test@12345"


def _create_user(driver) -> str:
    """Creates a new ESS-role system user linked to an existing employee,
    with a unique username each call, and returns that username.
    """
    username = f"testuser{int(time.time() * 1000)}"

    list_page = AdminUserListPage(driver).load()
    add_user_page = list_page.click_add()
    add_user_page.create_user(
        user_role="ESS",
        employee_search_text=EXISTING_EMPLOYEE_SEARCH_TEXT,
        status="Enabled",
        username=username,
        password=NEW_USER_PASSWORD,
    )

    confirmation = add_user_page.get_save_confirmation()
    logger.info("Created user '%s': %s", username, confirmation)
    return username


def test_create_new_user_and_validate_login(admin_login):
    """Test-Case-5: Navigate to the Admin menu, add a new user with valid
    details, log out, and attempt login with the newly created user.
    """
    username = _create_user(admin_login)

    home_page = AuthenticatedPage(admin_login)
    home_page.logout()

    login_page = LoginPage(admin_login).load()
    login_page.login(username, NEW_USER_PASSWORD)

    new_user_home = AuthenticatedPage(admin_login)
    assert new_user_home.is_authenticated_page_loaded(), (
        f"Expected the newly created user '{username}' to log in successfully"
    )
    logger.info("New user '%s' logged in successfully", username)


def test_new_user_appears_in_admin_user_list(admin_login):
    """Test-Case-6: Access Admin > User Management, search for the newly
    created user, and confirm it is found in the listing.
    """
    username = _create_user(admin_login)

    list_page = AdminUserListPage(admin_login).load()
    list_page.search_by_username(username)

    assert list_page.is_user_listed(username), (
        f"Expected '{username}' to be found in the system users list"
    )
    logger.info("Confirmed '%s' appears in the user listing", username)
