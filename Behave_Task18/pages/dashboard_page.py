"""Page Object for the Zen Portal dashboard page (post-login landing page)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Encapsulates locators/actions for the dashboard, including logout."""

    URL_FRAGMENT = "/dashboard"

    DASHBOARD_HEADING = (By.XPATH, "//*[normalize-space()='Dashboard']")
    CLOSE_POPUP_BUTTON = (
        By.XPATH,
        "//button[@aria-label='Close popup' or normalize-space()='Close popup']",
    )
    PROFILE_NAME = (By.CSS_SELECTOR, "p.avatar-profile-name")
    LOGOUT_MENU_ITEM = (By.XPATH, "//*[normalize-space()='Log out']")

    def __init__(self, driver: WebDriver, timeout: int = 15):
        super().__init__(driver, timeout)

    def is_loaded(self) -> bool:
        """Explicit wait until the URL reflects the dashboard route."""
        return self.wait_for_url_contains(self.URL_FRAGMENT)

    def is_dashboard_heading_visible(self) -> bool:
        return self.is_visible_within_timeout(self.DASHBOARD_HEADING)

    def dismiss_promo_popup_if_present(self) -> "DashboardPage":
        """The dashboard sometimes shows a promo modal on first login; close
        it if present so it doesn't block later clicks. Uses a short
        explicit wait so it does not stall the scenario when the popup
        never appears.
        """
        if self.is_visible_within_timeout(self.CLOSE_POPUP_BUTTON, timeout=4):
            self.safe_click(self.CLOSE_POPUP_BUTTON)
        return self

    def open_profile_menu(self) -> "DashboardPage":
        """Open the profile dropdown that contains the Log out item.

        Retries the click once if the menu doesn't open right away, to
        absorb timing flakiness on the live site.
        """
        if self.is_visible_within_timeout(self.LOGOUT_MENU_ITEM, timeout=2):
            return self  # menu already open

        self.safe_click(self.PROFILE_NAME)

        if not self.is_visible_within_timeout(self.LOGOUT_MENU_ITEM, timeout=5):
            self.safe_click(self.PROFILE_NAME)
            self.wait_for_visible(self.LOGOUT_MENU_ITEM)

        return self

    def logout(self) -> "DashboardPage":
        """Full logout flow: dismiss popup, open profile menu, click Log out."""
        self.dismiss_promo_popup_if_present()
        self.open_profile_menu()
        self.safe_click(self.LOGOUT_MENU_ITEM)
        return self