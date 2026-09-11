"""Test-Case-7: Verify login with invalid credentials.

Scenario: enter incorrect email/password, attempt to login. Expected:
login should fail, and an appropriate error message should be
displayed.
"""

from data.users import INVALID_EMAIL, INVALID_PASSWORD
from utils.logger import get_logger

logger = get_logger(__name__)


def test_login_with_invalid_credentials_fails(login_page):
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)

    assert not login_page.is_logged_in(timeout=5), (
        "Expected login to fail with invalid credentials, but the "
        "logged-in avatar appeared"
    )
    assert login_page.URL_FRAGMENT in login_page.driver.current_url, (
        "Expected to remain on the sign-in page after a failed login"
    )

    error_message = login_page.get_error_message()
    assert error_message, "Expected an error message to be displayed"
    assert "incorrect" in error_message.lower(), (
        f"Expected an 'incorrect email or password'-style message, got {error_message!r}"
    )

    logger.info("Invalid login correctly rejected with message: %r", error_message)
