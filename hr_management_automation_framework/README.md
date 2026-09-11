# HR Management Web Application Automation Framework

Automated test suite for the [OrangeHRM demo](https://opensource-demo.orangehrmlive.com/),
built with **Python + Selenium WebDriver + pytest**, using the **Page
Object Model** for its object-oriented structure.

## Architecture

```
hr_management_automation_framework/
├── pages/
│   ├── base_page.py             # BasePage: explicit waits + generic label-based field/dropdown helpers
│   ├── authenticated_page.py     # AuthenticatedPage: main menu + logout, shared by every logged-in page
│   ├── login_page.py              # LoginPage
│   ├── admin_user_page.py          # AdminUserListPage + AddUserPage
│   ├── my_info_page.py              # MyInfoPage (+ its 10 sub-tabs)
│   ├── leave_page.py                 # LeaveModulePage + AssignLeavePage
│   └── claim_page.py                  # ClaimModulePage + SubmitClaimPage
├── data/
│   ├── login_credentials.csv     # External data source for Test-Case-1 (data-driven requirement)
│   ├── data_loader.py             # Reads the CSV into plain dicts
│   └── users.py                   # Admin credentials + a known test employee
├── utils/
│   ├── exceptions.py             # Custom exception hierarchy
│   └── logger.py                 # Logging config (console + logs/test_run.log)
├── tests/
│   ├── conftest.py               # driver fixture (--target-browser CLI option), admin_login fixture
│   ├── test_login.py              # Test-Case-1 (CSV-driven, parametrized)
│   ├── test_home_url.py            # Test-Case-2
│   ├── test_login_fields.py         # Test-Case-3
│   ├── test_main_menu.py             # Test-Case-4
│   ├── test_user_management.py        # Test-Case-5, Test-Case-6
│   ├── test_forgot_password.py         # Test-Case-7
│   ├── test_my_info.py                  # Test-Case-8
│   ├── test_leave.py                     # Test-Case-9
│   └── test_claim.py                      # Test-Case-10
├── requirements.txt
├── pytest.ini
└── logs/                          # (git-ignored) test_run.log written here
```

### Design principles

- **Object-oriented programming**: every page is a class inheriting
  `BasePage` (or `AuthenticatedPage`, which itself extends `BasePage`
  with the header/menu behavior every logged-in page shares).
- **Exception handling**: `BasePage` wraps raw Selenium exceptions into a
  custom hierarchy (`ElementInteractionError`, `LoginFailedError`,
  `UserManagementError`, `LeaveAssignmentError`, `ClaimSubmissionError`)
  with messages describing the business action that failed.
- **Data-driven testing**: `data/login_credentials.csv` is the
  "structured external data source" Test-Case-1 asks for -
  `data/data_loader.py` reads it and `test_login.py` parametrizes over
  every row, so adding a new credential combination means editing a
  spreadsheet, not test code.
- **Keyword-driven testing**: `BasePage` exposes generic, reusable
  actions - `type_into_field`, `select_dropdown`,
  `select_autocomplete_suggestion`, `select_first_dropdown_option` - all
  keyed by a field's **visible label text**. OrangeHRM's entire UI (the
  "oxd" component library) structures every form field identically
  (`<div class="oxd-input-group"><label>...</label><input>/select</div>`),
  so this one mechanism drives the Add User, Assign Leave, and Submit
  Claim forms without hardcoding a different brittle locator per field
  per page.
- **Explicit waits**: every interaction goes through `WebDriverWait`
  (`find`, `click`, `is_visible`, `wait_until_url_contains`,
  `wait_until_url_changes`) - no blind `time.sleep()` calls.
- **Logging of results**: `utils/logger.py` configures a shared logger
  writing to both the console and `logs/test_run.log`; every test and
  page action logs what it did and what it found, independent of
  pytest's own HTML report.
- **Cross-browser support**: the `driver` fixture accepts a
  `--target-browser` CLI option (`chrome` default, `firefox` supported)
  so the same suite can run against either browser without code changes.
  It's deliberately not named the more obvious `--browser` - that name
  collides with a built-in option some other pytest plugins
  (`pytest-playwright`, `pytest-selenium`) register automatically the
  moment they're installed anywhere in the active virtual environment,
  even one shared with unrelated projects.

## 1. Setup (PyCharm or VS Code)

1. Open the `hr_management_automation_framework` folder as its own
   project root.
2. Create a virtual environment.
3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

   Selenium 4's built-in Selenium Manager downloads a matching
   ChromeDriver automatically on first run (Google Chrome must be
   installed). For Firefox, geckodriver is resolved the same way if
   Firefox is installed.

## 2. Running the tests

```powershell
pytest
```

Runs headless by default, writes a self-contained HTML report to
`reports/report.html`, and appends detailed step logs to
`logs/test_run.log`.

```powershell
$env:HEADLESS = "false"; pytest          # watch the browser locally
pytest --target-browser=firefox           # run against Firefox instead
pytest tests/test_claim.py -v             # run a single test case
```