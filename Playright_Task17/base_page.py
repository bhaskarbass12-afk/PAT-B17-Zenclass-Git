from playwright.sync_api import Page, Locator
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

DEFAULT_TIMEOUT_MS = 15000


class BasePage:


    def __init__(self, page: Page, timeout: int = DEFAULT_TIMEOUT_MS):
        self.page = page
        self.timeout = timeout

    def wait_for_visible(self, locator: Locator) -> Locator:

        locator.wait_for(state="visible", timeout=self.timeout)
        return locator

    def wait_for_hidden(self, locator: Locator) -> Locator:

        locator.wait_for(state="hidden", timeout=self.timeout)
        return locator

    def is_visible_within_timeout(self, locator: Locator) -> bool:

        try:
            locator.wait_for(state="visible", timeout=self.timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def wait_for_url_fragment(self, fragment: str) -> bool:

        try:
            self.page.wait_for_url(f"**{fragment}**", timeout=self.timeout)
            return True
        except PlaywrightTimeoutError:
            return False
