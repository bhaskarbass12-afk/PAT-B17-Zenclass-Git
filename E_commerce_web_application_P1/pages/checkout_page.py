from typing import Dict, List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.exceptions import CheckoutError


class CheckoutPage(BasePage):
    """Encapsulates locators/actions across the checkout information,
    overview, and confirmation steps.
    """

    STEP_TWO_URL_FRAGMENT = "checkout-step-two.html"
    COMPLETE_URL_FRAGMENT = "checkout-complete.html"

    # Step One: information form
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Step Two: order overview
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    TOTAL_LABEL = (By.CSS_SELECTOR, "[data-test='total-label']")
    FINISH_BUTTON = (By.ID, "finish")

    # Step Three: confirmation
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fills in the Step One information form (does not submit it)."""
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)

    def continue_to_overview(self) -> None:
        self.click(self.CONTINUE_BUTTON)
        if not self.wait_until_url_contains(self.STEP_TWO_URL_FRAGMENT):
            raise CheckoutError("Checkout did not advance to the order overview step")

    def get_overview_items(self) -> List[Dict[str, str]]:
        """Returns the items listed on the Step Two order overview as a
        list of {"name", "price", "quantity"} dicts.
        """
        names = self.driver.find_elements(*self.ITEM_NAME)
        prices = self.driver.find_elements(*self.ITEM_PRICE)
        quantities = self.driver.find_elements(*self.ITEM_QUANTITY)
        return [
            {"name": n.text, "price": p.text, "quantity": q.text}
            for n, p, q in zip(names, prices, quantities)
        ]

    def get_total_label(self) -> str:
        return self.get_text(self.TOTAL_LABEL)

    def take_screenshot(self, path: str) -> None:
        """Captures a screenshot of the current step (used to record the
        order summary before finalizing the order).
        """
        self.driver.save_screenshot(path)

    def finish(self) -> None:
        self.click(self.FINISH_BUTTON)
        if not self.wait_until_url_contains(self.COMPLETE_URL_FRAGMENT):
            raise CheckoutError("Checkout did not reach the order confirmation step")

    def get_confirmation_message(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)