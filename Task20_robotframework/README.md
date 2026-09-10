# Task 20 - Sauce Demo Login / Cart / Checkout (Robot Framework)

Stack: **Robot Framework + SeleniumLibrary**, keyword-driven testing, run
against [Sauce Demo](https://www.saucedemo.com/).

```
task20_sauce_demo_robot/
  resources/
    keywords.robot        # Reusable keywords: Login, Add To Cart, Checkout, verifications
  tests/
    sauce_demo_tests.robot  # The 4 required test cases
  requirements.txt
  .gitignore
```

## 1. Open the project in PyCharm

1. `File > Open...` and select the `task20_sauce_demo_robot` folder.
2. Create a virtual environment: `File > Settings > Project: task20_sauce_demo_robot
   > Python Interpreter > Add Interpreter > Add Local Interpreter > Virtualenv`.
3. (Optional) Install the **RobotFramework** plugin from the JetBrains
   marketplace for syntax highlighting, keyword auto-complete, and a
   right-click "Run" action on `.robot` files.
4. Open the PyCharm terminal and install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

   This installs Robot Framework, SeleniumLibrary, and Selenium. Selenium
   4's built-in Selenium Manager downloads a matching ChromeDriver
   automatically on first run, so no separate driver install is needed
   (Google Chrome itself must be installed).

## 2. Run the suite

With the RobotFramework plugin, right-click `tests/sauce_demo_tests.robot`
and choose **Run**. Without the plugin, use the terminal:

```powershell
robot -d results tests/sauce_demo_tests.robot
```

`-d results` writes `log.html`, `report.html`, and `output.xml` into a
`results/` folder (git-ignored).

Runs headless by default (`${BROWSER}` is `headlesschrome` in
`resources/keywords.robot`). To watch it run locally instead:

```powershell
robot -d results -v BROWSER:chrome tests/sauce_demo_tests.robot
```

## 3. Test cases

| # | Test case | What it verifies |
|---|---|---|
| 1 | `Login With Valid Credentials Lands On Products Page` | Logs in with `standard_user` / `secret_sauce` and confirms the user lands on the Products page. |
| 2 | `Login With Invalid Credentials Shows Error Message` | Confirms the "Epic sadface..." error banner appears for bad credentials. |
| 3 | `Add Single Product To Cart` | Adds one product, then confirms it's listed in the cart with the correct quantity. |
| 4 | `Checkout With Multiple Products` | Adds three products, proceeds through checkout, and confirms all three items (and their quantities) appear correctly in the checkout overview. |

## 4. How the task's requirements map to the implementation

| Requirement | Implementation |
|---|---|
| Variables for URL, credentials, and other reusable data | `*** Variables ***` section in `resources/keywords.robot` (`${URL}`, `${VALID_USERNAME}`, `${VALID_PASSWORD}`, all locators) |
| SeleniumLibrary for web interactions | `Open Browser`, `Input Text`, `Input Password`, `Click Element`, `Wait Until Element Is Visible`, `Get Text`, `Get WebElements`, etc. |
| BuiltIn for standard operations | `Log`, `Should Be Equal As Strings`, `Should Contain`, `Create List` |
| Keyword-driven testing with reusable keywords | Every action (`Login`, `Add Product To Cart By Name`, `Proceed To Checkout`, `Fill Checkout Information`, ...) is a named keyword in `resources/keywords.robot`, imported via `Resource` and composed by the test cases |

## Notes on locators

Product "Add to cart" buttons are located by matching the product's
**visible name text** (via XPath) rather than guessing the button's
generated `id` (e.g. `add-to-cart-sauce-labs-backpack`), so the suite
doesn't depend on exactly reproducing Sauce Demo's id-slugging scheme for
every product name. This also sidesteps a real quirk found while inspecting
the live site: the product name `<div>` on the inventory page has a
trailing space in its `class` attribute (`class="inventory_item_name "`)
that isn't present on the cart/checkout pages - the XPath locators use
`contains(@class, ...)` and `normalize-space()` to stay robust to that.

Each test case opens its own browser (`Test Setup`) and closes it
afterward (`Test Teardown`), so tests don't leak session state between
each other.
