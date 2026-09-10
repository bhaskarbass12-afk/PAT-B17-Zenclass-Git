*** Settings ***
Documentation     Reusable, keyword-driven building blocks for the Sauce
...               Demo login / cart / checkout test suite (Task 20).
...
...               Built with Robot Framework's SeleniumLibrary (web
...               interactions), BuiltIn (assertions, logging), and
...               Collections (list comparisons for cart contents).
Library           SeleniumLibrary
Library           BuiltIn
Library           Collections

*** Variables ***
${BROWSER}                 headlesschrome
${URL}                      https://www.saucedemo.com/
${VALID_USERNAME}           standard_user
${VALID_PASSWORD}           secret_sauce
${INVALID_LOGIN_ERROR}      Epic sadface: Username and password do not match any user in this service

${USERNAME_FIELD}           id:user-name
${PASSWORD_FIELD}           id:password
${LOGIN_BUTTON}             id:login-button
${ERROR_MESSAGE}            css:[data-test="error"]
${PAGE_TITLE}               css:.title

${CART_BADGE}                css:.shopping_cart_badge
${CART_LINK}                 css:.shopping_cart_link
${CHECKOUT_BUTTON}           id:checkout
${CART_ITEM_NAME}            css:.inventory_item_name

${FIRST_NAME_FIELD}          id:first-name
${LAST_NAME_FIELD}           id:last-name
${POSTAL_CODE_FIELD}         id:postal-code
${CONTINUE_BUTTON}           id:continue
${FINISH_BUTTON}             id:finish

*** Keywords ***
Open Browser To Sauce Demo
    [Documentation]    Opens a browser and navigates to the Sauce Demo login
    ...                page.
    [Arguments]    ${browser}=${BROWSER}
    Open Browser    ${URL}    ${browser}
    Set Window Size    1920    1080
    Wait Until Element Is Visible    ${USERNAME_FIELD}    timeout=10s

Login
    [Documentation]    Fills in the login form with the given credentials
    ...                and submits it.
    [Arguments]    ${username}    ${password}
    Input Text        ${USERNAME_FIELD}    ${username}
    Input Password    ${PASSWORD_FIELD}    ${password}
    Click Element      ${LOGIN_BUTTON}
    Log    Submitted login form for user '${username}'    console=${True}

Verify User Lands On Products Page
    [Documentation]    Confirms a successful login by checking the URL and
    ...                the "Products" page title.
    Wait Until Location Contains    inventory.html    timeout=10s
    Wait Until Element Is Visible    ${PAGE_TITLE}    timeout=10s
    ${page_title}=    Get Text    ${PAGE_TITLE}
    Should Be Equal As Strings    ${page_title}    Products
    ...    msg=Expected to land on the Products page after login
    Log    Landed on the products page    console=${True}

Verify Login Error Message Is Displayed
    [Documentation]    Confirms the appropriate error banner is shown after
    ...                an invalid login attempt.
    [Arguments]    ${expected_message}=${INVALID_LOGIN_ERROR}
    Wait Until Element Is Visible    ${ERROR_MESSAGE}    timeout=10s
    ${actual_message}=    Get Text    ${ERROR_MESSAGE}
    Should Contain    ${actual_message}    ${expected_message}
    Log    Login error confirmed: ${actual_message}    console=${True}

Add Product To Cart By Name
    [Documentation]    Clicks the "Add to cart" button for the inventory
    ...                item whose visible name matches ${product_name}.
    ...                Locates the button by matching the product's name
    ...                text (normalized to ignore incidental whitespace in
    ...                the page's own markup) rather than guessing the
    ...                button's generated id.
    [Arguments]    ${product_name}
    ${add_button}=    Set Variable
    ...    xpath://div[@class="inventory_item"][.//div[contains(@class, "inventory_item_name") and normalize-space(text())="${product_name}"]]//button
    Wait Until Element Is Visible    ${add_button}    timeout=10s
    Click Element    ${add_button}
    Log    Added '${product_name}' to the cart    console=${True}

Add Multiple Products To Cart
    [Documentation]    Adds every product name in @{product_names} to the
    ...                cart, one at a time.
    [Arguments]    @{product_names}
    FOR    ${product_name}    IN    @{product_names}
        Add Product To Cart By Name    ${product_name}
    END

Verify Cart Badge Count
    [Documentation]    Confirms the shopping cart icon shows the expected
    ...                number of items.
    [Arguments]    ${expected_count}
    Wait Until Element Is Visible    ${CART_BADGE}    timeout=10s
    ${badge_count}=    Get Text    ${CART_BADGE}
    Should Be Equal As Strings    ${badge_count}    ${expected_count}
    ...    msg=Expected the cart badge to show ${expected_count} item(s)

Open Cart
    [Documentation]    Opens the shopping cart page.
    Click Element    ${CART_LINK}
    Wait Until Location Contains    cart.html    timeout=10s

Get Cart Item Names
    [Documentation]    Returns the list of product names currently shown on
    ...                the cart or checkout-overview page.
    ${elements}=    Get WebElements    ${CART_ITEM_NAME}
    ${result}=    Create List
    FOR    ${element}    IN    @{elements}
        ${text}=    Get Text    ${element}
        Append To List    ${result}    ${text}
    END
    RETURN    ${result}

Verify Product Listed In Cart
    [Documentation]    Confirms ${product_name} appears among the items
    ...                currently listed on the cart/checkout page.
    [Arguments]    ${product_name}
    ${names}=    Get Cart Item Names
    List Should Contain Value    ${names}    ${product_name}
    ...    msg=Expected '${product_name}' to be listed in the cart

Verify Cart Contains Products
    [Documentation]    Confirms the items listed on the cart/checkout page
    ...                are exactly the given @{product_names} (regardless of
    ...                order), with no extra or missing products.
    [Arguments]    @{product_names}
    ${names}=    Get Cart Item Names
    Lists Should Be Equal    ${names}    ${product_names}
    ...    msg=Cart contents do not match the expected products
    ...    ignore_order=${True}

Verify Cart Item Quantity
    [Documentation]    Confirms the quantity shown for ${product_name} on
    ...                the cart/checkout page equals ${expected_quantity}.
    [Arguments]    ${product_name}    ${expected_quantity}
    ${quantity_locator}=    Set Variable
    ...    xpath://div[@class="cart_item"][.//div[contains(@class, "inventory_item_name") and normalize-space(text())="${product_name}"]]//div[@class="cart_quantity"]
    ${actual_quantity}=    Get Text    ${quantity_locator}
    Should Be Equal As Strings    ${actual_quantity}    ${expected_quantity}
    ...    msg=Expected quantity ${expected_quantity} for '${product_name}', got ${actual_quantity}

Proceed To Checkout
    [Documentation]    Clicks Checkout from the cart page and waits for the
    ...                checkout information form to load.
    Click Element    ${CHECKOUT_BUTTON}
    Wait Until Location Contains    checkout-step-one.html    timeout=10s

Fill Checkout Information
    [Documentation]    Fills in the checkout Step One information form and
    ...                continues to the order overview (Step Two).
    [Arguments]    ${first_name}    ${last_name}    ${postal_code}
    Input Text    ${FIRST_NAME_FIELD}    ${first_name}
    Input Text    ${LAST_NAME_FIELD}    ${last_name}
    Input Text    ${POSTAL_CODE_FIELD}    ${postal_code}
    Click Element    ${CONTINUE_BUTTON}
    Wait Until Location Contains    checkout-step-two.html    timeout=10s

Close Sauce Demo Browser
    [Documentation]    Closes all open browser windows.
    Close All Browsers