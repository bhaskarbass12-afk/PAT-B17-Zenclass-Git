"""Test-Case-5: Random selection of products and data extraction."""

from pages.products_page import ProductsPage
from utils.test_helpers import pick_random_products


def test_random_product_selection_extracts_correct_data(logged_in_products_page):
    """Randomly selects 4 of the 6 listed products and verifies their
    name/price data was extracted accurately - i.e. it matches what the
    page itself currently reports for those exact products.
    """
    products_page: ProductsPage = logged_in_products_page

    all_products = products_page.get_products()
    assert len(all_products) == 6, f"Expected 6 products, found {len(all_products)}"

    selected = pick_random_products(all_products, count=4)
    print(f"Randomly selected products: {selected}")  # visible with pytest -s / in the HTML report

    current_by_name = {p["name"]: p["price"] for p in products_page.get_products()}
    for product in selected:
        assert product["name"] in current_by_name, (
            f"Selected product '{product['name']}' is missing from the page"
        )
        assert current_by_name[product["name"]] == product["price"], (
            f"Price mismatch for '{product['name']}': "
            f"extracted '{product['price']}', page shows '{current_by_name[product['name']]}'"
        )
