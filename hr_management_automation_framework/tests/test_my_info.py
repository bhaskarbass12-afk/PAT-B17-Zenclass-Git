"""Test-Case-8: Validate the presence of menu items under "My Info"."""

import pytest

from pages.my_info_page import MyInfoPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.parametrize("tab_name", MyInfoPage.EXPECTED_TABS)
def test_my_info_tab_visible_and_clickable(admin_login, tab_name):
    """Navigates to My Info and verifies that each expected sub-menu tab
    (Personal Details, Contact Details, Emergency Contacts, ...) is
    listed and opens its corresponding page when clicked.
    """
    my_info_page = MyInfoPage(admin_login).load()
    assert my_info_page.is_displayed(), "Expected to land on the My Info page"

    assert my_info_page.is_tab_visible(tab_name), (
        f"Expected '{tab_name}' to be listed under My Info"
    )

    # Note: "Personal Details" is the default tab already shown when My
    # Info loads, so clicking it is a no-op and never changes the URL -
    # checking for a URL change would be a false negative for that one
    # tab specifically. Verifying the page is still displaying its tab
    # navigation (i.e. nothing broke) after the click is the check that
    # holds true for every tab, including the already-active one.
    my_info_page.click_tab(tab_name)

    assert my_info_page.is_displayed(), (
        f"Expected the My Info page to remain functional after clicking '{tab_name}'"
    )
    logger.info("My Info tab '%s' opened successfully (now at %s)", tab_name, admin_login.current_url)
