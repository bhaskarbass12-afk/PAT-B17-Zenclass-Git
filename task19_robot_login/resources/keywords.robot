*** Settings ***
Documentation     Reusable, keyword-driven building blocks for the
...               RobotSpareBin Industries Inc. intranet login/logout suite.
...
...               Built with Robot Framework's SeleniumLibrary (web
...               interactions) and BuiltIn (assertions, logging, status
...               checks) as required by Task 19.
Library           SeleniumLibrary
Library           BuiltIn

*** Variables ***
${BROWSER}              headlesschrome
${URL}                  https://robotsparebinindustries.com
# Published demo credentials, shown directly on the login page's own help
# text ("Psst... You can login using 'maria' as username and
# 'thoushallnotpass' as password."). Not a secret - this is Robocorp's
# public training site.
${VALID_USERNAME}       maria
${VALID_PASSWORD}       thoushallnotpass
${USERNAME_FIELD}       id:username
${PASSWORD_FIELD}       id:password
${LOGIN_BUTTON}         css:button[type="submit"]
${LOGOUT_BUTTON}        id:logout
${ERROR_MESSAGE}        css:.alert-warning

*** Keywords ***
Open Browser To Intranet
    [Documentation]    Opens a browser and navigates to the RobotSpareBin
    ...                Industries intranet login page.
    [Arguments]    ${browser}=${BROWSER}
    Open Browser    ${URL}    ${browser}
    Set Window Size    1920    1080
    Wait Until Element Is Visible    ${USERNAME_FIELD}    timeout=10s
    Log    Browser opened and navigated to ${URL}    console=${True}

Login
    [Documentation]    Fills in the login form with the given credentials
    ...                and submits it.
    [Arguments]    ${username}    ${password}
    Input Text        ${USERNAME_FIELD}    ${username}
    Input Password    ${PASSWORD_FIELD}    ${password}
    Click Button       ${LOGIN_BUTTON}
    Log    Submitted login form for user '${username}'    console=${True}

Verify Login Successful
    [Documentation]    Confirms the intranet landing page loaded by checking
    ...                for the presence of the Log out button.
    Wait Until Element Is Visible    ${LOGOUT_BUTTON}    timeout=10s
    ${is_logged_in}=    Run Keyword And Return Status
    ...    Element Should Be Visible    ${LOGOUT_BUTTON}
    Should Be True    ${is_logged_in}
    ...    msg=Expected the Log out button to be visible after a successful login
    Log    Login successful; Log out button is visible    console=${True}

Verify Login Failed
    [Documentation]    Confirms the "Invalid username or password." warning
    ...                is shown when credentials are rejected.
    Wait Until Element Is Visible    ${ERROR_MESSAGE}    timeout=10s
    ${message}=    Get Text    ${ERROR_MESSAGE}
    Should Contain    ${message}    Invalid username or password.
    Log    Invalid-credentials warning confirmed: ${message}    console=${True}

Logout
    [Documentation]    Logs out of the intranet and confirms the login form
    ...                reappears.
    Click Button    ${LOGOUT_BUTTON}
    Wait Until Element Is Visible    ${USERNAME_FIELD}    timeout=10s
    Element Should Be Visible    ${USERNAME_FIELD}
    Log    Logged out; login form is visible again    console=${True}

Close Intranet Browser
    [Documentation]    Closes all open browser windows.
    Close All Browsers