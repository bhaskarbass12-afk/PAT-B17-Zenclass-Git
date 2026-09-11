"""Test-Case-10: Validate logout functionality.

Scenario: log in using valid credentials, click the Logout option.
Expected: the user should be logged out successfully and redirected to
the login or homepage.

Note: this site's logged-in avatar dropdown labels the action "Sign
Out" rather than "Logout" - confirmed by live inspection - but it's the
same logout mechanism the brief describes.
"""

from utils.logger import get_logger

logger = get_logger(__name__)


def test_logout_after_valid_login(logged_in_home_page):
    assert logged_in_home_page.is_logged_in(timeout=10), (
        "Precondition failed: expected to already be logged in before "
        "testing logout"
    )

    # sign_out() itself raises LogoutFailedError if anything about the
    # flow doesn't behave as expected (no active session, "Login" never
    # reappearing, etc.) - letting it propagate gives a clear failure.
    logged_in_home_page.sign_out()

    assert not logged_in_home_page.is_logged_in(timeout=5), (
        "Expected the logged-in avatar to disappear after signing out"
    )
    assert logged_in_home_page.is_any_visible(logged_in_home_page.LOGIN_BUTTON), (
        "Expected the header's 'Login' button to reappear after signing out"
    )

    logger.info("Logout succeeded, current URL: %s", logged_in_home_page.driver.current_url)
