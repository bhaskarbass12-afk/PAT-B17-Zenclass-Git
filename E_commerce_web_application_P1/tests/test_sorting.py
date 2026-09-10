"""Test-Case-9: Validate sorting functionality on the products page."""

import pytest


def _sort_by_price_low_to_high(products):
    return sorted(products, key=lambda p: float(p["price"].replace("$", "")))


def _sort_by_name_z_to_a(products):
    return sorted(products, key=lambda p: p["name"], reverse=True)


@pytest.mark.parametrize(
    "sort_option,expected_order_fn",
    [
        ("price_low_to_high", _sort_by_price_low_to_high),
        ("name_z_to_a", _sort_by_name_z_to_a),
    ],
    ids=["price_low_to_high", "name_z_to_a"],
)
def test_sorting_updates_product_order(logged_in_products_page, sort_option, expected_order_fn):
    """Changes the sort option and verifies the product list re-orders to
    match the expected sort behavior for that option.
    """
    products_page = logged_in_products_page
    baseline = products_page.get_products()
    expected_names = [p["name"] for p in expected_order_fn(baseline)]

    products_page.sort_by(sort_option)

    actual_names = products_page.get_product_names()
    assert actual_names == expected_names, (
        f"Expected order {expected_names} for '{sort_option}', got {actual_names}"
    )
