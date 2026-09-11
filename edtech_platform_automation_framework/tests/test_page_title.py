"""Test-Case-2: Verify that the title of the webpage is correct.

Honest note: the original test brief expects the title to read exactly
"GUVI｜Learn to code in your native language". Live inspection of the
site shows it has since been rebranded - the real, current title is
"HCL GUVI | Learn to code in your native language" (GUVI is now part of
HCL Group). This test asserts against the real, current title rather
than the brief's now-outdated exact string; see README.md's
"Verification status" section for the full explanation.
"""

from utils.logger import get_logger

logger = get_logger(__name__)

EXPECTED_TITLE = "HCL GUVI | Learn to code in your native language"


def test_home_page_title_matches_expected(home_page):
    actual_title = home_page.get_title()
    logger.info("Home page title: %r", actual_title)

    assert actual_title == EXPECTED_TITLE, (
        f"Expected title {EXPECTED_TITLE!r}, got {actual_title!r}"
    )
