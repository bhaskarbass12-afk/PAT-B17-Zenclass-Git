import pytest

# ---------------------------------------------------------------------------
# a) Successful Login  -- POSITIVE
# ---------------------------------------------------------------------------
class TestSuccessfulLogin:

    def test_valid_login_succeeds(self, login_page):
        login_page.login()  # valid credentials
        assert not login_page.check_for_unsuccessful_login(), \
            "Valid credentials should not show an error message."
        assert not login_page.is_on_login_page(), \
            "After a valid login the app should leave the login page."

# ---------------------------------------------------------------------------
# b) Unsuccessful Login  -- NEGATIVE
# ---------------------------------------------------------------------------
class TestUnsuccessfulLogin:

    @pytest.mark.parametrize("email,password", [
        ("wrong@gmail.com", "WrongPass@123"),   # both wrong
        ("bhaskarbass12@gmail.com", "badpass"),  # wrong password
        ("notanemail", "SomePass@1"),            # malformed email
    ])
    def test_invalid_login_shows_error(self, login_page, email, password):
        login_page.login(email, password)
        assert login_page.check_for_unsuccessful_login(), \
            f"Expected an error for invalid login: {email}"
        assert login_page.is_on_login_page(), \
            "Failed login must stay on the login page."

    def test_empty_fields_do_not_login(self, login_page):
        login_page.login("", "")
        assert login_page.is_on_login_page(), \
            "Empty credentials must not log the user in."

# ---------------------------------------------------------------------------
# c) Validate Username / Password input boxes
# ---------------------------------------------------------------------------
class TestInputBoxes:

    def test_input_boxes_are_displayed(self, login_page):   # POSITIVE
        assert login_page.is_email_input_displayed(), "Email box should be visible."
        assert login_page.is_password_input_displayed(), "Password box should be visible."

    def test_email_box_accepts_text(self, login_page):      # POSITIVE
        typed = login_page.type_email("sample@test.com")
        assert typed == "sample@test.com", "Email box should hold the typed value."

    def test_password_box_accepts_text(self, login_page):   # POSITIVE
        typed = login_page.type_password("Secret@123")
        assert typed == "Secret@123", "Password box should hold the typed value."

    def test_password_is_masked(self, login_page):          # NEGATIVE-ish check
        box = login_page.wait.until(
            __import__("selenium.webdriver.support.expected_conditions",
                       fromlist=["visibility_of_element_located"])
            .visibility_of_element_located(login_page.password)
        )
        assert box.get_attribute("type") == "password", \
            "Password field must mask input (type='password')."

# ---------------------------------------------------------------------------
# d) Validate Submit button
# ---------------------------------------------------------------------------
class TestSubmitButton:

    def test_submit_button_is_enabled(self, login_page):    # POSITIVE
        assert login_page.is_submit_enabled(), "Submit button should be enabled/clickable."

    def test_submit_with_empty_form_stays(self, login_page):  # NEGATIVE
        login_page.click_submit()
        assert login_page.is_on_login_page(), \
            "Submitting an empty form should not navigate away."

# ---------------------------------------------------------------------------
# e) Validate Logout functionality
# ---------------------------------------------------------------------------
class TestLogout:

    def test_logout_returns_to_login(self, logged_in_home):  # POSITIVE
        logged_in_home.logout()
        assert logged_in_home.is_logout_successful(), \
            "After logout the login screen should be shown again."
