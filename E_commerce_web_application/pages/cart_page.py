from typing import Dict, List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class CartPage(BasePage):
    """Encapsulates locators/actions for https://www.saucedemo.com/cart.html."""

    URL_FRAGMENT = "cart.html"

    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def is_displayed(self) -> bool:
        return self.wait_until_url_contains(self.URL_FRAGMENT)

    def get_cart_items(self) -> List[Dict[str, str]]:
        """Returns every item currently in the cart as a list of
        {"name", "price", "quantity"} dicts. Returns an empty list (rather
        than raising) when the cart has no items - an empty cart is a
        valid, expected state, not an error.
        """
        names = self.driver.find_elements(*self.ITEM_NAME)
        prices = self.driver.find_elements(*self.ITEM_PRICE)
        quantities = self.driver.find_elements(*self.ITEM_QUANTITY)
        return [
            {"name": n.text, "price": p.text, "quantity": q.text}
            for n, p, q in zip(names, prices, quantities)
        ]

    def proceed_to_checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)
