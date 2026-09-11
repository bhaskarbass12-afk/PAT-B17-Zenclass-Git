from typing import Dict, List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from utils.exceptions import ProductNotFoundError


class ProductsPage(BasePage):
    """Encapsulates locators/actions for https://www.saucedemo.com/inventory.html."""

    URL_FRAGMENT = "inventory.html"

    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_LINK = (By.ID, "reset_sidebar_link")

    # Maps friendly sort names to the <select>'s actual option values, so
    # tests can say "price_low_to_high" instead of memorizing "lohi".
    SORT_OPTIONS = {
        "name_a_to_z": "az",
        "name_z_to_a": "za",
        "price_low_to_high": "lohi",
        "price_high_to_low": "hilo",
    }

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def is_displayed(self) -> bool:
        return self.wait_until_url_contains(self.URL_FRAGMENT) and self.is_visible(
            self.PAGE_TITLE
        )

    def get_products(self) -> List[Dict[str, str]]:
        """Returns every listed product as a list of {"name", "price"}
        dicts, in current display order.
        """
        names = [el.text for el in self.find_all(self.ITEM_NAME)]
        prices = [el.text for el in self.driver.find_elements(*self.ITEM_PRICE)]
        return [{"name": n, "price": p} for n, p in zip(names, prices)]

    def get_product_names(self) -> List[str]:
        return [product["name"] for product in self.get_products()]

    def add_product_to_cart(self, product_name: str) -> None:
        """Clicks the "Add to cart" button for the item whose visible name
        matches `product_name`. Locates the button by matching the
        product's name text (normalized to ignore incidental whitespace in
        the page's own markup) rather than guessing its generated id.
        """
        locator = (
            By.XPATH,
            "//div[@class='inventory_item']"
            "[.//div[contains(@class, 'inventory_item_name') and "
            f"normalize-space(text())='{product_name}']]//button",
        )
        if not self.is_visible(locator, timeout=5):
            raise ProductNotFoundError(
                f"Could not find product '{product_name}' to add to cart"
            )
        self.click(locator)

    def get_cart_count(self) -> int:
        """Returns the number shown on the cart badge, or 0 if the badge
        is absent (empty cart never renders a badge at all).
        """
        if not self.is_visible(self.CART_BADGE, timeout=3):
            return 0
        return int(self.get_text(self.CART_BADGE))

    def is_cart_icon_visible(self) -> bool:
        return self.is_visible(self.CART_LINK, timeout=5)

    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    def sort_by(self, option: str) -> None:
        """Applies a sort order. `option` is one of the keys in
        SORT_OPTIONS (e.g. "price_low_to_high"), or a raw option value.
        """
        value = self.SORT_OPTIONS.get(option, option)
        dropdown = self.find(self.SORT_DROPDOWN)
        Select(dropdown).select_by_value(value)

    def open_menu(self) -> None:
        self.click(self.MENU_BUTTON)

    def logout(self) -> None:
        """Convenience wrapper: opens the menu and clicks Logout."""
        self.open_menu()
        self.click(self.LOGOUT_LINK)

    def reset_app_state(self) -> None:
        self.open_menu()
        self.click(self.RESET_LINK)