"""Test-Case-4: Check cart icon visibility."""


def test_cart_icon_visible_on_products_page(logged_in_products_page):
    """The cart icon should be visible on the product listing page and
    should remain accessible at all times after login - including after
    interacting with the page (e.g. sorting), since it's part of the
    persistent header rather than something that can be scrolled/sorted
    away.
    """
    products_page = logged_in_products_page

    assert products_page.is_cart_icon_visible(), (
        "Expected the cart icon to be visible on the products page"
    )

    products_page.sort_by("price_low_to_high")
    assert products_page.is_cart_icon_visible(), (
        "Expected the cart icon to remain visible after sorting products"
    )
