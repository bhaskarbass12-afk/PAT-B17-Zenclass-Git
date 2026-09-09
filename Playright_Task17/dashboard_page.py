from playwright.sync_api import Page

from base_page import BasePage


class DashboardPage(BasePage):

    URL_FRAGMENT = "/dashboard"

    def __init__(self, page: Page, timeout: int = 15000):
        super().__init__(page, timeout)
        self.dashboard_heading = page.get_by_text("Dashboard", exact=True)
        self.close_popup_button = page.get_by_role("button", name="Close popup")
        self.profile_name = page.locator("p.avatar-profile-name")
        self.logout_menu_item = page.get_by_text("Log out", exact=True)

    def is_loaded(self) -> bool:

        return self.wait_for_url_fragment(self.URL_FRAGMENT)

    def dismiss_promo_popup_if_present(self) -> "DashboardPage":

        if self.is_visible_within_timeout(self.close_popup_button):
            self.close_popup_button.click()
        return self

    def open_profile_menu(self) -> "DashboardPage":
        self.wait_for_visible(self.profile_name)
        self.profile_name.click()
        self.wait_for_visible(self.logout_menu_item)
        return self

    def logout(self) -> "DashboardPage":
       
        self.dismiss_promo_popup_if_present()
        self.open_profile_menu()
        self.logout_menu_item.click()
        return self