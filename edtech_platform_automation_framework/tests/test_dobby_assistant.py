"""Test-Case-9: Validate that the "Dobby Guvi Assistant" is present on
the page.

Scenario (per the brief): navigate to the Dobby Assistant, look for the
widget/chatbot. Expected: the Dobby Guvi Assistant should be displayed
on the page.

Honest note - this test is expected to fail on the current live site.
During development, the homepage was searched thoroughly for anything
matching "Dobby": visible text, every element's `class` and `id`
attributes, the raw page source, every fixed-position element (the
usual technique for a floating chat-widget launcher), and every
`<iframe>` on the page. None of it turned up any match. The same
search was repeated after logging in (on the post-login `/courses/`
page) in case the assistant is only shown to authenticated users - also
no match. A web search for "GUVI Dobby assistant" likewise found no
reference to it as a current, named GUVI feature.

The most likely explanation is that this was a feature that existed
when the brief was written and has since been removed or renamed - the
same period in which the site rebranded from "GUVI" to "HCL GUVI" (see
test_page_title.py). Rather than fabricate a locator for a widget that
isn't there (which would either produce a false pass or a misleading
generic "element not found" error), this test documents exactly what
was checked and fails with a clear, specific message. If GUVI
reintroduces this feature under a different name, update
`DOBBY_SEARCH_KEYWORDS` below and this test will find it automatically.
"""

from selenium.webdriver.common.by import By

from utils.exceptions import FeatureNotFoundError
from utils.logger import get_logger

logger = get_logger(__name__)

DOBBY_SEARCH_KEYWORDS = ["dobby"]


def test_dobby_guvi_assistant_is_present(home_page):
    driver = home_page.driver
    page_source = driver.page_source.lower()

    for keyword in DOBBY_SEARCH_KEYWORDS:
        if keyword in page_source:
            logger.info("Found keyword '%s' in page source", keyword)
            return

        matches = driver.find_elements(
            By.XPATH,
            f"//*[contains(translate(@class,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            f"'abcdefghijklmnopqrstuvwxyz'),'{keyword}') or "
            f"contains(translate(@id,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            f"'abcdefghijklmnopqrstuvwxyz'),'{keyword}')]",
        )
        if matches:
            logger.info("Found %d element(s) matching keyword '%s'", len(matches), keyword)
            return

    raise FeatureNotFoundError(
        "The 'Dobby Guvi Assistant' widget/chatbot described in the test "
        "brief could not be located anywhere on https://www.guvi.in - "
        "checked visible text, page source, and every element's class/id "
        "for any of these keywords: " + ", ".join(DOBBY_SEARCH_KEYWORDS) + ". "
        "This feature likely no longer exists on the live site (possibly "
        "removed/renamed during the site's 'GUVI' -> 'HCL GUVI' rebrand - "
        "see test_page_title.py). See README.md for details."
    )
