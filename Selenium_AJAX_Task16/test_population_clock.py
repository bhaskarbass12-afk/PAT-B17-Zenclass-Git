import re
import time

from population_clock_page import PopulationClockPage


def test_page_loads_successfully(driver):
    page = PopulationClockPage(driver).load()
    assert "theworldcounts.com" in driver.current_url


def test_population_counter_is_displayed(driver):
    page = PopulationClockPage(driver).load()
    element = page.get_population_counter_element()
    assert element.is_displayed()


def test_population_count_has_valid_format(driver):
    page = PopulationClockPage(driver).load()
    text = page.get_population_count_text()
    assert re.fullmatch(r"[\d,]+", text), f"Unexpected population format: {text}"


def test_population_count_is_reasonable(driver):
    page = PopulationClockPage(driver).load()
    count = page.get_population_count()
    # Sanity bound: current world population should be in the billions.
    assert 7_000_000_000 <= count <= 12_000_000_000


def test_population_counter_title_text(driver):
    page = PopulationClockPage(driver).load()
    title = page.get_counter_title_text()
    assert title.lower() == "world population"


def test_population_count_increases_over_time(driver):
    page = PopulationClockPage(driver).load()
    first = page.get_population_count()
    time.sleep(3)
    second = page.get_population_count()
    assert second >= first
