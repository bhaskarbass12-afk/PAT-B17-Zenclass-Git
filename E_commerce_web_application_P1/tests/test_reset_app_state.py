"""Test-Case-10: Validate "Reset App State" functionality."""

from pages.cart_page import CartPage


def test_reset_app_state_clears_cart(logged_in_products_page):
    """After adding products to the cart, using the menu's "Reset App
    State" should clear all cart items and return the app to its default,
    no-selections state.
    """
    products_page = logged_in_products_page
    products_page.add_product_to_cart("Sauce Labs Backpack")
    products_page.add_product_to_cart("Sauce Labs Bike Light")
    assert products_page.get_cart_count() == 2, "Expected 2 items in the cart before reset"

    products_page.reset_app_state()

    assert products_page.get_cart_count() == 0, "Expected the cart to be empty after reset"

    products_page.open_cart()
    cart_page = CartPage(products_page.driver)
    assert cart_page.get_cart_items() == [], (
        "Expected no items listed on the cart page after resetting app state"
    )
