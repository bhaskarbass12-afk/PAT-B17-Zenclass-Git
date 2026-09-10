Feature: Zen Portal Login and Logout
  As a Zen Portal user
  I want to log in and log out reliably
  So that I can trust the authentication flow works correctly

  # Covers all required report sections:
  #   c) Validate Username, Password Input box
  Scenario: Validate the username and password input boxes
    Given I am on the Zen Portal login page
    When I enter "sample.user@example.com" in the email field
    And I enter "SamplePass123" in the password field
    Then the email field should contain "sample.user@example.com"
    And the password field should contain "SamplePass123"
    And the password field should be of type "password"

  # d) Validate Submit button working or not
  Scenario: Validate the submit button is working
    Given I am on the Zen Portal login page
    Then the submit button should be visible and enabled
    When I enter invalid credentials and click sign in
    Then an error message should be displayed

  # b) Unsuccessful Login
  Scenario: Unsuccessful login with invalid credentials
    Given I am on the Zen Portal login page
    When I login with email "invalid_user_test_zenclass@example.com" and password "WrongPassword!123"
    Then an error message should be displayed
    And I should remain on the login page

  # a) Successful Login
  @requires_credentials
  Scenario: Successful login with valid credentials
    Given I am on the Zen Portal login page
    When I login with valid credentials
    Then I should be redirected to the dashboard page

  # e) Validate the functionality of the Logout button
  @requires_credentials
  Scenario: Logout functionality works correctly
    Given I am logged in to the Zen Portal
    When I click the logout button
    Then I should be redirected back to the login page