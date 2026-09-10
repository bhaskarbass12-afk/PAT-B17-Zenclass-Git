"""Test-Case-3: Validate logout functionality."""

from pages.login_page import LoginPage


def test_logout_button_visible_and_functional(logged_in_products_page):
    """Checks whether the Logout menu item is visible after login, and
    whether clicking it properly logs the user out (redirecting back to
    the login screen).
    """
    products_page = logged_in_products_page

    products_page.open_menu()
    assert products_page.is_visible(products_page.LOGOUT_LINK), (
        "Expected the Logout link to be visible after opening the menu"
    )

    products_page.click(products_page.LOGOUT_LINK)

    login_page = LoginPage(products_page.driver)
    assert login_page.is_displayed(), (
        "Expected to be redirected to the login screen after logging out"
    )
