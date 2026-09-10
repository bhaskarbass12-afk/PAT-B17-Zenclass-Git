*** Settings ***
Documentation     Task 19 - RobotSpareBin Industries Inc. intranet
...               login/logout test suite, built with Robot Framework and
...               SeleniumLibrary using keyword-driven testing.
...
...               Covers:
...               - Opening the browser and navigating to the application.
...               - Inputting valid credentials and submitting the form.
...               - Verifying successful login via a specific landing-page
...                 element (the Log out button).
...               - Logging out of the application.
Resource          ../resources/keywords.robot
Test Setup        Open Browser To Intranet
Test Teardown     Close Intranet Browser

*** Test Cases ***
Successful Login With Valid Credentials
    [Documentation]    Logs in with the published demo credentials, verifies
    ...                the intranet landing page loads, then logs out again.
    [Tags]    login    smoke
    Login    ${VALID_USERNAME}    ${VALID_PASSWORD}
    Verify Login Successful
    Logout

Unsuccessful Login With Invalid Credentials
    [Documentation]    Verifies that invalid credentials are rejected with a
    ...                clear error message and the user stays on the login
    ...                page.
    [Tags]    login    negative
    Login    invalid_user    invalid_password
    Verify Login Failed
