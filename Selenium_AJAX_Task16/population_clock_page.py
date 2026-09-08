from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PopulationClockPage:
    """Page Object Model for the world population clock page."""

    URL = (
        "https://www.theworldcounts.com/challenges/planet-earth/"
        "state-of-the-planet/world-population-clock-live"
    )

    # Locators (XPATH only)
    POPULATION_COUNTER_XPATH = (
        "//div[contains(@class,'big-counter')]//div[contains(@class,'counter-ticker')]"
    )
    COUNTER_TITLE_XPATH = (
        "//div[contains(@class,'big-counter')]//h1[contains(@class,'counter-title')]"
    )

    def __init__(self, driver, wait_timeout: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)

    def load(self) -> "PopulationClockPage":
        """Navigate to the population clock page."""
        self.driver.get(self.URL)
        return self

    def get_population_counter_element(self):
        """Explicit wait until the population counter element is visible."""
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.POPULATION_COUNTER_XPATH))
        )

    def get_population_count_text(self) -> str:
        """Return the raw population count text, e.g. '8,272,021,845'."""
        return self.get_population_counter_element().text.strip()

    def get_population_count(self) -> int:
        """Return the population count parsed as an integer."""
        text = self.get_population_count_text()
        return int(text.replace(",", ""))

    def get_counter_title_element(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.COUNTER_TITLE_XPATH))
        )

    def get_counter_title_text(self) -> str:
        return self.get_counter_title_element().text.strip()






