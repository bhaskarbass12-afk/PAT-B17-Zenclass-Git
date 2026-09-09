"""Task 17 - Zen Portal Login/Logout test suite.

Stack: Microsoft Playwright (Python) + Pytest + Page Object Model + Explicit
Wait, per the task requirements. An HTML report is generated automatically
under reports/report.html (see pytest.ini).

Covers all required report sections:
    a) Successful Login
    b) Unsuccessful Login
    c) Validate Username, Password Input box
    d) Validate Submit button working or not
    e) Validate the functionality of the Logout button
"""

from playwright.sync_api import expect

# Deliberately fake credentials for the negative-login test. Confirmed (via
# manual exploration) that the portal shows the same "Invalid email!" banner
# for any unrecognized email/password combination, so no real account is
# needed to exercise this path.
INVALID_EMAIL = "invalid_user_test_zenclass@example.com"
INVALID_PASSWORD = "WrongPassword!123"


def test_username_and_password_input_box(login_page):
    """c) Validate Username, Password Input box."""
    expect(login_page.email_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.password_input).to_have_attribute("type", "password")

    login_page.enter_email("sample.user@example.com")
    login_page.enter_password("SamplePass123")

    assert login_page.email_input.input_value() == "sample.user@example.com"
    assert login_page.password_input.input_value() == "SamplePass123"


def test_submit_button_working(login_page):
    """d) Validate Submit button working or not."""
    expect(login_page.submit_button).to_be_visible()
    assert login_page.is_submit_button_enabled()

    login_page.enter_email(INVALID_EMAIL)
    login_page.enter_password(INVALID_PASSWORD)
    login_page.click_sign_in()

    # A working submit button triggers a server round trip; the app then
    # renders the credential-error banner for bad input.
    assert login_page.is_error_displayed()


def test_unsuccessful_login(login_page):
    """b) Unsuccessful Login."""
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)

    assert login_page.is_error_displayed()
    assert "invalid" in login_page.get_error_text().lower()
    assert "/login" in login_page.page.url


def test_successful_login(login_page, dashboard_page, valid_credentials):
    """a) Successful Login."""
    email, password = valid_credentials
    login_page.login(email, password)

    assert dashboard_page.is_loaded()
    dashboard_page.dismiss_promo_popup_if_present()
    expect(dashboard_page.dashboard_heading).to_be_visible()


def test_logout_functionality(login_page, dashboard_page, valid_credentials):
    """e) Validate the functionality of the Logout button."""
    email, password = valid_credentials
    login_page.login(email, password)
    assert dashboard_page.is_loaded()

    dashboard_page.logout()

    assert login_page.wait_for_url_fragment("/login")
    expect(login_page.email_input).to_be_visible()