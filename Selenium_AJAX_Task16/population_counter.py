import argparse
import time
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from population_clock_page import PopulationClockPage

POLL_INTERVAL_SECONDS = 1

def build_driver(headless: bool = False) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

def main() -> None:
    parser = argparse.ArgumentParser(description="Live world population counter (console).")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run Chrome in headless mode.",
    )
    args = parser.parse_args()

    driver = build_driver(headless=args.headless)
    page = PopulationClockPage(driver)

    try:
        page.load()
        print("Extracting live world population count. Press CTRL+C to stop.\n")
        while True:
            try:
                count_text = page.get_population_count_text()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] World Population: {count_text}")
            except (TimeoutException, StaleElementReferenceException):
                print("Population counter temporarily unavailable, retrying...")
            time.sleep(POLL_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nStopped by user (CTRL+C). Exiting gracefully.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
