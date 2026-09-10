"""Step definitions for Task 18 - Zen Portal Login/Logout (Behave + Allure).

Stack: Selenium WebDriver + Behave + Page Object Model + Explicit Wait, per
the task requirements. Allure attaches a step-by-step breakdown of each
scenario (see the @allure.step decorators) plus a screenshot on failure
(see features/environment.py's after_step hook).
"""

import allure
from behave import given, then, when

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


# Deliberately fake credentials for the negative-login scenarios. Confirmed
# (via manual exploration) that the portal shows the same "Invalid email!"
# banner for any unrecognized email/password combination, so no real
# account is needed to exercise this path.
INVALID_EMAIL = "invalid_user_test_zenclass@example.com"
INVALID_PASSWORD = "WrongPassword!123"


def _login_page(context) -> LoginPage:
    if not hasattr(context, "login_page"):
        context.login_page = LoginPage(context.driver)
    return context.login_page


def _dashboard_page(context) -> DashboardPage:
    if not hasattr(context, "dashboard_page"):
        context.dashboard_page = DashboardPage(context.driver)
    return context.dashboard_page


@given("I am on the Zen Portal login page")
def step_open_login_page(context):
    with allure.step("Navigate to the Zen Portal login page"):
        _login_page(context).load()


@when('I enter "{email}" in the email field')
def step_enter_email(context, email):
    with allure.step(f'Enter "{email}" in the email field'):
        _login_page(context).enter_email(email)


@when('I enter "{password}" in the password field')
def step_enter_password(context, password):
    with allure.step("Enter password in the password field"):
        _login_page(context).enter_password(password)


@then('the email field should contain "{expected}"')
def step_check_email_value(context, expected):
    with allure.step("Verify the email field retains the entered value"):
        assert _login_page(context).get_email_value() == expected


@then('the password field should contain "{expected}"')
def step_check_password_value(context, expected):
    with allure.step("Verify the password field retains the entered value"):
        assert _login_page(context).get_password_value() == expected


@then('the password field should be of type "{expected_type}"')
def step_check_password_type(context, expected_type):
    with allure.step(f'Verify the password field has type "{expected_type}"'):
        assert _login_page(context).get_password_field_type() == expected_type


@then("the submit button should be visible and enabled")
def step_check_submit_button(context):
    with allure.step("Verify the submit button is visible and enabled"):
        page = _login_page(context)
        assert page.is_submit_button_visible()
        assert page.is_submit_button_enabled()


@when("I enter invalid credentials and click sign in")
def step_invalid_login_click(context):
    with allure.step("Enter invalid credentials and click Sign in"):
        _login_page(context).login(INVALID_EMAIL, INVALID_PASSWORD)


@then("an error message should be displayed")
def step_check_error_displayed(context):
    with allure.step("Verify the credential-error banner is displayed"):
        assert _login_page(context).is_error_displayed()


@when('I login with email "{email}" and password "{password}"')
def step_login_with_credentials(context, email, password):
    with allure.step(f'Log in with email "{email}"'):
        _login_page(context).login(email, password)


@then("I should remain on the login page")
def step_remain_on_login(context):
    with allure.step("Verify the browser stayed on the login page"):
        assert "/login" in context.driver.current_url


@when("I login with valid credentials")
def step_login_with_valid_credentials(context):
    with allure.step("Log in with configured valid credentials"):
        assert context.zen_email and context.zen_password, (
            "ZEN_EMAIL/ZEN_PASSWORD not configured"
        )
        _login_page(context).login(context.zen_email, context.zen_password)


@then("I should be redirected to the dashboard page")
def step_check_dashboard_loaded(context):
    with allure.step("Verify the dashboard page loaded after login"):
        dashboard = _dashboard_page(context)
        assert dashboard.is_loaded()
        dashboard.dismiss_promo_popup_if_present()
        assert dashboard.is_dashboard_heading_visible()


@given("I am logged in to the Zen Portal")
def step_given_logged_in(context):
    with allure.step("Log in to the Zen Portal with valid credentials"):
        assert context.zen_email and context.zen_password, (
            "ZEN_EMAIL/ZEN_PASSWORD not configured"
        )
        _login_page(context).load()
        _login_page(context).login(context.zen_email, context.zen_password)
        assert _dashboard_page(context).is_loaded()


@when("I click the logout button")
def step_click_logout(context):
    with allure.step("Click the Log out menu item"):
        _dashboard_page(context).logout()


@then("I should be redirected back to the login page")
def step_check_back_on_login(context):
    with allure.step("Verify the browser returned to the login page"):
        login = _login_page(context)
        assert login.wait_for_url_fragment("/login")
        assert login.is_email_input_visible()