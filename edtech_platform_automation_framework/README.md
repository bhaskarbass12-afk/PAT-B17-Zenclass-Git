# EdTech Platform (GUVI) Automation Framework

Automated test suite for the [GUVI / HCL GUVI platform](https://www.guvi.in/),
built with **Python + Selenium WebDriver + pytest**, using the **Page
Object Model** for its object-oriented structure.

## Architecture

```
edtech_platform_automation_framework/
├── pages/
│   ├── base_page.py       # BasePage: explicit waits + shared header behavior
│   │                       #   (Login/Sign up buttons, avatar menu, sign out)
│   ├── home_page.py        # HomePage: title, homepage nav items
│   ├── login_page.py        # LoginPage: email/password form, error message
│   └── register_page.py      # RegisterPage: confirms Sign-Up navigation
├── data/
│   └── users.py            # VALID_* (from .env), INVALID_* (hardcoded, fake)
├── utils/
│   ├── exceptions.py       # Custom exception hierarchy
│   └── logger.py           # Logging config (console + logs/test_run.log)
├── tests/
│   ├── conftest.py         # driver fixture (--target-browser), home_page/
│   │                        #   login_page/valid_credentials/logged_in_home_page
│   ├── test_home_url.py            # Test-Case-1
│   ├── test_page_title.py           # Test-Case-2
│   ├── test_login_button.py          # Test-Case-3
│   ├── test_signup_button.py          # Test-Case-4
│   ├── test_signup_navigation.py       # Test-Case-5
│   ├── test_login_valid.py              # Test-Case-6
│   ├── test_login_invalid.py             # Test-Case-7
│   ├── test_menu_items.py                 # Test-Case-8
│   ├── test_dobby_assistant.py             # Test-Case-9 (known gap, see below)
│   └── test_logout.py                       # Test-Case-10
├── requirements.txt
├── pytest.ini
├── .env.example             # Copy to .env and fill in a real GUVI login
└── logs/                     # (git-ignored) test_run.log written here
```

### Design principles

- **Object-oriented programming**: every page is a class inheriting
  `BasePage`. GUVI's header (Login/Sign up buttons, the logged-in
  avatar menu) appears on every page in the site, not just the
  homepage, so that shared behavior lives once in `BasePage` rather than
  being duplicated across `HomePage`/`LoginPage`/`RegisterPage`.
- **Exception handling**: `BasePage` wraps raw Selenium exceptions into
  a custom hierarchy (`ElementInteractionError`, `LoginFailedError`,
  `LogoutFailedError`, `NavigationError`, `FeatureNotFoundError`) with
  messages describing the business action that failed, not just "element
  not found".
- **Explicit waits, no hidden-duplicate traps**: every interaction goes
  through `WebDriverWait` - no blind `time.sleep()` calls. A real,
  confirmed quirk of this site's markup is that many header elements
  (nav items, Login/Sign up buttons, the avatar) are rendered *twice* at
  once - a desktop copy and a hidden mobile copy. A locator that just
  grabs "the first match" can silently grab the hidden one. `first_visible`
  / `click_first_visible` / `is_any_visible` explicitly scan every match
  and act on whichever one is actually displayed, rather than assuming
  DOM order.
- **Secrets kept out of source control**: Test-Case-6 and Test-Case-10
  require a real GUVI account. Real credentials are never hardcoded -
  they're read from environment variables (`GUVI_EMAIL`/`GUVI_PASSWORD`)
  via a local, git-ignored `.env` file. Tests that need them are
  `pytest.skip`'d (not failed) if `.env` isn't configured, so the rest
  of the suite still runs cleanly without a real account.
- **Logging of results**: `utils/logger.py` configures a shared logger
  writing to both the console and `logs/test_run.log`; every test logs
  what it did and what it found, independent of pytest's own HTML report.
- **Cross-browser support**: the `driver` fixture accepts a
  `--target-browser` CLI option (`chrome` default, `firefox` supported).

## 1. Setup

1. Open this folder as its own project root (PyCharm or VS Code).
2. Create a virtual environment and install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

   Selenium 4's built-in Selenium Manager downloads a matching
   ChromeDriver automatically on first run (Google Chrome must be
   installed).

3. Copy `.env.example` to `.env` and fill in a real GUVI account:

   ```
   GUVI_EMAIL=your_email@example.com
   GUVI_PASSWORD=your_password
   ```

   `.env` is git-ignored and will never be committed. Without it,
   Test-Case-6 and Test-Case-10 (the two that require an actual login)
   are skipped; every other test case runs normally.

## 2. Running the tests

```powershell
pytest
```

Runs headless by default, writes a self-contained HTML report to
`reports/report.html`, and appends detailed step logs to
`logs/test_run.log`.

```powershell
$env:HEADLESS = "false"; pytest              # watch the browser locally
pytest --target-browser=firefox               # run against Firefox instead
pytest tests/test_login_valid.py -v            # run a single test case
```

## 3. Test case reference

| # | Test case | File |
|---|---|---|
| 1 | Home URL is valid and loads without error | `test_home_url.py` |
| 2 | Homepage title is correct | `test_page_title.py` |
| 3 | Login button visible and clickable | `test_login_button.py` |
| 4 | Sign-Up button visible and redirects to /register/ | `test_signup_button.py` |
| 5 | Sign-Up navigation lands on the register page | `test_signup_navigation.py` |
| 6 | Login with valid credentials | `test_login_valid.py` |
| 7 | Login with invalid credentials shows an error | `test_login_invalid.py` |
| 8 | Key menu items ("Courses", "LIVE Classes", "Practice") are visible | `test_menu_items.py` |
| 9 | "Dobby Guvi Assistant" is present | `test_dobby_assistant.py` |
| 10 | Logout functionality | `test_logout.py` |

## 4. Verification status and honest notes

Two real discrepancies between the test brief and the live site were
found while building this suite, both most likely explained by GUVI's
rebrand to **HCL GUVI** sometime after the brief was written:

- **Test-Case-2 (title)**: the brief expects
  `"GUVI｜Learn to code in your native language"`. The live title is
  actually `"HCL GUVI | Learn to code in your native language"`. The
  test asserts against the real, current title.
- **Test-Case-9 (Dobby Guvi Assistant)**: this feature could not be
  found anywhere on the live site - not on the homepage, not on the
  post-login dashboard, not in the raw page source, not among any
  fixed-position widgets or iframes. See `test_dobby_assistant.py`'s
  module docstring for the full list of what was checked. **This test
  is expected to fail** - it documents the gap with a specific
  `FeatureNotFoundError` message rather than faking a locator for a
  widget that isn't there, or silently skipping it as if nothing were
  wrong.

Everything else was confirmed against the live site's real DOM and
passes, including some behavior that isn't obvious from the brief
alone:

- The header's "Login" and "Sign up" controls are `<button>` elements
  with no `href` (client-side routing), not `<a>` tags.
- The actual login submit control is `<a id="login-btn">`, not a
  `<button>`.
- Logging in does **not** trigger an OTP or reCAPTCHA challenge for a
  normal automated session (both exist elsewhere on the site, but
  weren't triggered by this login flow during testing).
- After a successful login the user lands on `/courses/`, not a URL
  containing "profile" or "dashboard".
- The logged-in state is signaled by a `.gravatar-wrap` avatar
  replacing the Login/Sign up buttons in the header; clicking it opens
  a dropdown whose logout action is labeled **"Sign Out"**, not
  "Logout".
- Invalid login shows the message "Incorrect Email or Password" in a
  `.invalid-feedback` element under both the email and password fields.
