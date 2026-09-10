"""Behave environment hooks for the Task 18 Zen Portal BDD suite.

Responsibilities:
- Put the project root on sys.path so `pages.*` is importable from
  features/steps regardless of the working directory Behave (or PyCharm)
  is launched from.
- Own the Selenium WebDriver lifecycle (one browser per test run).
- Skip scenarios tagged @requires_credentials when ZEN_EMAIL/ZEN_PASSWORD
  are not configured, instead of failing the whole run.
- Attach a screenshot to the Allure report whenever a step fails.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import allure
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Load ZEN_EMAIL / ZEN_PASSWORD from a local .env file (see .env.example).
# The .env file is git-ignored; never commit real credentials.
load_dotenv()


def before_all(context):
    options = Options()
    if os.getenv("HEADLESS", "true").lower() != "false":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")

    # Selenium 4's built-in Selenium Manager resolves/downloads the matching
    # chromedriver automatically, so no manual driver management is needed.
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(0)  # rely solely on the POM's explicit waits

    context.zen_email = os.getenv("ZEN_EMAIL")
    context.zen_password = os.getenv("ZEN_PASSWORD")


def before_scenario(context, scenario):
    if "requires_credentials" in scenario.effective_tags and not (
        context.zen_email and context.zen_password
    ):
        scenario.skip(
            "ZEN_EMAIL / ZEN_PASSWORD not set. Copy .env.example to .env and "
            "fill in a real Zen Portal login to run this scenario."
        )
        return

    # The browser is reused across scenarios for speed, so a successful
    # login in one scenario would otherwise leave the next scenario
    # already authenticated. Clear cookies/storage so every scenario
    # starts from a logged-out state.
    try:
        context.driver.delete_all_cookies()
        context.driver.execute_script(
            "window.localStorage.clear(); window.sessionStorage.clear();"
        )
    except Exception:
        pass  # nothing to clear yet on the very first scenario (blank page)

def after_step(context, step):
    if step.status == "failed":
        try:
            allure.attach(
                context.driver.get_screenshot_as_png(),
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            # Attaching a screenshot is best-effort; never mask the real
            # step failure with a screenshot-capture error.
            pass


def after_all(context):
    context.driver.quit()