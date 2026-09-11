"""Test-Case-8: Complete checkout and validate order."""

import os
from datetime import datetime

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")


def test_complete_checkout_and_validate_order(logged_in_products_page):
    """Adds a product, proceeds through checkout with user details,
    captures a screenshot of the order summary, finalizes the order, and
    verifies the confirmation message.
    """
    products_page = logged_in_products_page
    products_page.add_product_to_cart("Sauce Labs Backpack")
    products_page.open_cart()

    cart_page = CartPage(products_page.driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(products_page.driver)
    checkout_page.fill_information("John", "Doe", "12345")
    checkout_page.continue_to_overview()

    overview_items = checkout_page.get_overview_items()
    assert len(overview_items) == 1, "Expected exactly one item in the order summary"
    assert overview_items[0]["name"] == "Sauce Labs Backpack", (
        "Expected the order summary to reflect the correct product"
    )

    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    screenshot_path = os.path.join(
        SCREENSHOT_DIR, f"order_summary_{datetime.now():%Y%m%d_%H%M%S}.png"
    )
    checkout_page.take_screenshot(screenshot_path)
    assert os.path.exists(screenshot_path), "Expected the order-summary screenshot to be saved"

    checkout_page.finish()
    confirmation = checkout_page.get_confirmation_message()
    assert confirmation == "Thank you for your order!", (
        f"Unexpected confirmation message: '{confirmation}'"
    )
