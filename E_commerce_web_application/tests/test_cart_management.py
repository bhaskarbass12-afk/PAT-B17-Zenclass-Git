"""Test-Case-6 and Test-Case-7: adding products to the cart and validating
the cart's contents.
"""

from pages.cart_page import CartPage
from utils.test_helpers import pick_random_products


def test_add_random_products_updates_cart(logged_in_products_page):
    """Test-Case-6: Add 4 randomly selected products to the cart and
    verify the cart icon count matches and the correct items are listed.
    """
    products_page = logged_in_products_page
    selected = pick_random_products(products_page.get_products(), count=4)

    for product in selected:
        products_page.add_product_to_cart(product["name"])

    assert products_page.get_cart_count() == 4, "Expected the cart badge to show 4 items"

    products_page.open_cart()
    cart_page = CartPage(products_page.driver)
    assert cart_page.is_displayed()

    cart_names = {item["name"] for item in cart_page.get_cart_items()}
    expected_names = {p["name"] for p in selected}
    assert cart_names == expected_names, (
        f"Cart contents {cart_names} do not match the added products {expected_names}"
    )


def test_cart_details_match_added_products(logged_in_products_page):
    """Test-Case-7: Validate product details inside the cart.

    Adds 4 randomly selected products, then fetches the cart's listed
    product details and confirms they match exactly what was added
    (name, price, and quantity for each).
    """
    products_page = logged_in_products_page
    selected = pick_random_products(products_page.get_products(), count=4)
    expected_by_name = {p["name"]: p["price"] for p in selected}

    for product in selected:
        products_page.add_product_to_cart(product["name"])

    products_page.open_cart()
    cart_page = CartPage(products_page.driver)
    cart_items = cart_page.get_cart_items()

    assert len(cart_items) == len(selected), "Expected the cart to list all added products"
    for item in cart_items:
        assert item["name"] in expected_by_name, (
            f"Unexpected product '{item['name']}' found in the cart"
        )
        assert item["price"] == expected_by_name[item["name"]], (
            f"Price mismatch for '{item['name']}' in the cart"
        )
        assert item["quantity"] == "1", f"Expected quantity 1 for '{item['name']}'"
