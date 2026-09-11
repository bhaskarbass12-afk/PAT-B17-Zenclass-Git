"""Test-Case-4: Verify visibility and clickability of main menu items
after login.
"""

import pytest

from pages.authenticated_page import AuthenticatedPage
from utils.logger import get_logger

logger = get_logger(__name__)

EXPECTED_MENU_ITEMS = [
    "Admin",
    "PIM",
    "Leave",
    "Time",
    "Recruitment",
    "My Info",
    "Performance",
    "Dashboard",
]


@pytest.mark.parametrize("menu_item", EXPECTED_MENU_ITEMS)
def test_main_menu_item_visible_and_clickable(admin_login, menu_item):
    """Each specified menu item should be visible and functional after
    logging in with valid credentials.
    """
    home_page = AuthenticatedPage(admin_login)
    assert home_page.is_authenticated_page_loaded()

    assert home_page.is_menu_item_visible(menu_item), (
        f"Expected menu item '{menu_item}' to be visible"
    )
    assert home_page.is_menu_item_clickable(menu_item), (
        f"Expected menu item '{menu_item}' to be clickable"
    )
    logger.info("Menu item '%s' confirmed visible and clickable", menu_item)
