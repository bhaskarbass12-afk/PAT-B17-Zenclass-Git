"""Test-Case-8: Verify that menu items like "Courses", "LIVE Classes",
and "Practice" are displayed.

Scenario: check the homepage header/navigation bar, validate the
presence of key menu items. Expected: "Courses", "LIVE Classes", and
"Practice" should be visible and accessible.
"""

import pytest

from utils.logger import get_logger

logger = get_logger(__name__)

EXPECTED_MENU_ITEMS = ["LIVE Classes", "Courses", "Practice"]


@pytest.mark.parametrize("menu_item", EXPECTED_MENU_ITEMS)
def test_menu_item_is_visible(home_page, menu_item):
    assert home_page.is_menu_item_visible(menu_item), (
        f"Expected menu item '{menu_item}' to be visible in the homepage header"
    )
    logger.info("Menu item '%s' is visible", menu_item)
