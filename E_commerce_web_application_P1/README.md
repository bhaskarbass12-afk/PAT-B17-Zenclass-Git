# E-commerce Web Application Automation Framework

Automated test suite for [Sauce Demo](https://www.saucedemo.com/), built
with **Python + Selenium WebDriver + pytest**, using the **Page Object
Model** for its object-oriented structure.

## Architecture

```
ecommerce_automation_framework/
├── pages/                 # Page Objects (OOP layer)
│   ├── base_page.py        # BasePage: shared explicit waits + exception handling
│   ├── login_page.py        # LoginPage
│   ├── products_page.py     # ProductsPage (inventory, cart icon, menu)
│   ├── cart_page.py          # CartPage
│   └── checkout_page.py      # CheckoutPage (info -> overview -> confirmation)
├── data/
│   └── users.py             # Data-driven test data: predefined users, invalid credentials
├── utils/
│   ├── exceptions.py         # Custom exception hierarchy
│   └── test_helpers.py        # Shared helpers (e.g. random product selection)
├── tests/
│   ├── conftest.py            # pytest fixtures: driver lifecycle, logged-in session
│   ├── test_login.py           # Test-Case-1, Test-Case-2
│   ├── test_logout.py           # Test-Case-3
│   ├── test_cart_icon.py        # Test-Case-4
│   ├── test_product_selection.py # Test-Case-5
│   ├── test_cart_management.py   # Test-Case-6, Test-Case-7
│   ├── test_checkout.py          # Test-Case-8
│   ├── test_sorting.py           # Test-Case-9
│   └── test_reset_app_state.py   # Test-Case-10
├── requirements.txt
├── pytest.ini
└── screenshots/            # Captured order-summary screenshots (git-ignored)
```

### Design principles

- **Object-oriented programming**: every page of the site is modeled as a
  class (`LoginPage`, `ProductsPage`, `CartPage`, `CheckoutPage`), all
  inheriting shared behavior from `BasePage`. Locators are class
  attributes; actions and queries are methods. Tests never touch
  `driver.find_element` directly - they call page object methods.
- **Exception handling for test resilience**: `BasePage` wraps Selenium's
  low-level exceptions (`TimeoutException`, `StaleElementReferenceException`)
  into a small custom exception hierarchy (`utils/exceptions.py`) with
  messages that describe the *business action* that failed, not just "no
  such element". Page objects raise these (e.g. `ProductNotFoundError`,
  `LoginFailedError`, `CheckoutError`) instead of leaking raw Selenium
  tracebacks into test failures.
- **Data-driven testing**: `data/users.py` holds the predefined Sauce Demo
  accounts and invalid-credential combinations as plain data structures,
  consumed via `@pytest.mark.parametrize` in `test_login.py` - adding a
  new user/credential case means editing data, not test logic.
- **Keyword-driven testing**: every user action (`login`, `add_product_to_cart`,
  `sort_by`, `proceed_to_checkout`, `fill_information`, `reset_app_state`, ...)
  is a single, well-named "keyword" method on a page object. Test cases
  read as a sequence of these keywords rather than raw Selenium calls.
- **Reliable waits**: all interactions go through `BasePage`'s explicit
  `WebDriverWait`-based helpers (`find`, `click`, `is_visible`,
  `wait_until_url_contains`) - no blind `time.sleep()` calls.

## 1. Setup (PyCharm or VS Code)

1. Open the `ecommerce_automation_framework` folder as its own project
   root.
2. Create a virtual environment (PyCharm: `Settings > Project > Python
   Interpreter > Add Interpreter > Virtualenv`; VS Code: `python -m venv
   .venv` then select it as the interpreter).
3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

   Selenium 4's built-in Selenium Manager downloads a matching
   ChromeDriver automatically on first run - no manual driver setup is
   needed (Google Chrome itself must be installed).

## 2. Running the tests

```powershell
pytest
```

This runs the whole suite headless (default) and writes a self-contained
HTML report to `reports/report.html` (configured in `pytest.ini`).

To watch the browser locally instead of headless:

```powershell
$env:HEADLESS = "false"; pytest
```

Run a single test case, e.g. just the checkout flow:

```powershell
pytest tests/test_checkout.py -v
```

## 3. Test case reference

| # | Test case | File | What it verifies |
|---|---|---|---|
| 1 | Login with various predefined users | `test_login.py::test_login_with_predefined_users` | Each of the 6 Sauce Demo demo accounts behaves as expected (5 succeed, `locked_out_user` is rejected with its specific error). |
| 2 | Login with invalid credentials | `test_login.py::test_login_with_invalid_credentials` | Bad username/password combinations are denied with an error message and no navigation. |
| 3 | Validate logout functionality | `test_logout.py` | The Logout menu item is visible after opening the menu, and clicking it returns the user to the login screen. |
| 4 | Check cart icon visibility | `test_cart_icon.py` | The cart icon is visible on the products page and stays visible after interacting with the page. |
| 5 | Random selection of products and data extraction | `test_product_selection.py` | 4 of the 6 products are randomly selected and their extracted name/price data matches the page. |
| 6 | Add selected products to cart and validate | `test_cart_management.py::test_add_random_products_updates_cart` | Adding 4 random products updates the cart badge to 4 and lists exactly those products. |
| 7 | Validate product details inside the cart | `test_cart_management.py::test_cart_details_match_added_products` | The cart page's listed name/price/quantity for each item matches what was added. |
| 8 | Complete checkout and validate order | `test_checkout.py` | Checkout info form, order-summary screenshot capture, order finalization, and the "Thank you for your order!" confirmation. |
| 9 | Validate sorting functionality | `test_sorting.py` | "Price (low to high)" and "Name (Z to A)" sorting re-order the product list correctly. |
| 10 | Validate "Reset App State" | `test_reset_app_state.py` | After adding products, "Reset App State" clears the cart back to its default, empty state. |

## 4. Notes

- The suite uses Sauce Demo's own published demo accounts (all use the
  password `secret_sauce`) - these are intentionally public test
  credentials, not real secrets.
- Each test gets its own fresh browser session via the `driver` pytest
  fixture, which always calls `driver.quit()` in its teardown (inside a
  `try/finally`), guaranteeing the browser is closed after every test case
  regardless of pass/fail.
- Screenshots captured during checkout (Test-Case-8) are written to
  `screenshots/` (git-ignored) with a timestamped filename.
- After a run, `reports/report.html` contains the full self-contained test
  report - this is the file to share separately (e.g. via Google Drive)
  alongside the GitHub submission of the code itself.