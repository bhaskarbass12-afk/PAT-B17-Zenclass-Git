*** Settings ***
Documentation     Task 20 - Sauce Demo login / cart / checkout test suite,
...               built with Robot Framework and SeleniumLibrary using
...               keyword-driven testing.
Resource          ../resources/keywords.robot
Test Setup        Open Browser To Sauce Demo
Test Teardown     Close Sauce Demo Browser

*** Test Cases ***
Login With Valid Credentials Lands On Products Page
    [Documentation]    Test Case 1: Logs in with valid credentials
    ...                (standard_user / secret_sauce) and verifies the user
    ...                lands on the products page.
    [Tags]    login    smoke
    Login    ${VALID_USERNAME}    ${VALID_PASSWORD}
    Verify User Lands On Products Page

Login With Invalid Credentials Shows Error Message
    [Documentation]    Test Case 2: Attempts to log in with invalid
    ...                credentials and verifies that an appropriate error
    ...                message is displayed.
    [Tags]    login    negative
    Login    invalid_user    invalid_password
    Verify Login Error Message Is Displayed

Add Single Product To Cart
    [Documentation]    Test Case 3: After logging in with valid credentials,
    ...                adds a product to the cart and verifies the product
    ...                is correctly listed in the cart.
    [Tags]    cart
    Login    ${VALID_USERNAME}    ${VALID_PASSWORD}
    Verify User Lands On Products Page
    Add Product To Cart By Name    Sauce Labs Backpack
    Verify Cart Badge Count    1
    Open Cart
    Verify Product Listed In Cart    Sauce Labs Backpack
    Verify Cart Item Quantity    Sauce Labs Backpack    1

Checkout With Multiple Products
    [Documentation]    Test Case 4: Logs in with valid credentials, adds
    ...                multiple products to the cart, proceeds to the
    ...                checkout page, and verifies the correct items and
    ...                quantities are listed in the checkout summary.
    [Tags]    checkout
    Login    ${VALID_USERNAME}    ${VALID_PASSWORD}
    Verify User Lands On Products Page
    Add Multiple Products To Cart
    ...    Sauce Labs Backpack
    ...    Sauce Labs Bike Light
    ...    Sauce Labs Bolt T-Shirt
    Verify Cart Badge Count    3
    Open Cart
    Proceed To Checkout
    Fill Checkout Information    John    Doe    12345
    Verify Cart Contains Products
    ...    Sauce Labs Backpack
    ...    Sauce Labs Bike Light
    ...    Sauce Labs Bolt T-Shirt
    Verify Cart Item Quantity    Sauce Labs Backpack    1
    Verify Cart Item Quantity    Sauce Labs Bike Light    1
    Verify Cart Item Quantity    Sauce Labs Bolt T-Shirt    1