"""Test-Case-6: Verify login functionality with valid credentials.

Scenario: enter valid email and password on the login page, perform
login. Expected: the user should be logged in and redirected to their
profile/dashboard.
"""

from utils.exceptions import LoginFailedError
from utils.logger import get_logger

logger = get_logger(__name__)


def test_login_with_valid_credentials(login_page, valid_credentials):
    email, password = valid_credentials
    login_page.login(email, password)

    if not login_page.is_logged_in(timeout=10):
        raise LoginFailedError(
            f"Expected to be logged in after submitting valid credentials for "
            f"'{email}', but the header's avatar never appeared "
            f"(current URL: {login_page.driver.current_url!r})"
        )

    assert login_page.URL_FRAGMENT not in login_page.driver.current_url, (
        "Expected to be redirected away from the sign-in page after a "
        f"successful login, but still on {login_page.driver.current_url!r}"
    )

    logger.info(
        "Login with valid credentials succeeded, redirected to: %s",
        login_page.driver.current_url,
    )
