# Task 19 - RobotSpareBin Industries Intranet Login (Robot Framework)

Stack: **Robot Framework + SeleniumLibrary**, keyword-driven testing, run
against the [RobotSpareBin Industries Inc.](https://robotsparebinindustries.com)
intranet (Robocorp's public training site).

```
task19_robot_login/
  resources/
    keywords.robot     # Reusable keywords: Open Browser, Login, Verify Login, Logout
  tests/
    login_tests.robot  # Test cases that compose the keywords above
  requirements.txt
  .gitignore
```

## 1. Open the project in PyCharm

1. `File > Open...` and select the `task19_robot_login` folder.
2. Create a virtual environment: `File > Settings > Project: task19_robot_login
   > Python Interpreter > Add Interpreter > Add Local Interpreter > Virtualenv`.
3. (Optional but recommended) Install the **RobotFramework plugin** for
   PyCharm (Community or Professional both support it via the JetBrains
   plugin marketplace) - it adds syntax highlighting, keyword auto-complete,
   and a right-click "Run" action on `.robot` files.
4. Open the PyCharm terminal and install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

   This installs Robot Framework, SeleniumLibrary, and Selenium itself
   (a SeleniumLibrary dependency). Selenium 4's built-in Selenium Manager
   downloads a matching ChromeDriver automatically the first time the
   suite runs, so no separate driver install is needed (Google Chrome
   itself must be installed).

## 2. Run the suite

With the RobotFramework plugin, right-click `tests/login_tests.robot` and
choose **Run**. Without the plugin, use the PyCharm terminal:

```powershell
robot -d results tests/login_tests.robot
```

`-d results` writes `log.html`, `report.html`, and `output.xml` into a
`results/` folder (git-ignored) instead of cluttering the project root.

Runs headless by default (`${BROWSER}` is `headlesschrome` in
`resources/keywords.robot`). To watch the browser locally instead, change
that variable to `chrome`, or override it per run:

```powershell
robot -d results -v BROWSER:chrome tests/login_tests.robot
```

## 3. What the suite covers

| Task 19 requirement | Where it's implemented |
|---|---|
| Open the browser and navigate to the application | `Open Browser To Intranet` keyword (`Test Setup` in `login_tests.robot`) |
| Input valid credentials and submit the form | `Login` keyword |
| Verify login is successful via a specific landing-page element | `Verify Login Successful` (checks the `#logout` button) |
| Log out of the application | `Logout` keyword |
| SeleniumLibrary for web interactions | `Open Browser`, `Input Text`, `Input Password`, `Click Button`, `Wait Until Element Is Visible`, etc. |
| BuiltIn for standard operations | `Log`, `Should Be True`, `Should Contain`, `Run Keyword And Return Status` |
| Keyword-driven testing with reusable keywords | `resources/keywords.robot`, imported via `Resource` into the test suite |

An additional negative test (`Unsuccessful Login With Invalid Credentials`)
verifies the login form correctly rejects bad credentials, using the same
reusable keywords.

## Notes

- `maria` / `thoushallnotpass` are the intentionally public demo credentials
  displayed directly on the login page's own help text - not a real secret.
- Each test case opens its own browser (`Test Setup`) and closes it
  afterward (`Test Teardown`), so tests don't leak session state between
  each other.