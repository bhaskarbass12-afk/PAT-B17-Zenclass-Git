"""Reads the structured external login-credentials data source.

Test-Case-1 explicitly requires driving the login test from "a
structured external data source (e.g. Excel or CSV)" rather than data
hardcoded in Python. This module is the single place that reads
`login_credentials.csv`, so the test module itself only ever deals with
plain dictionaries.
"""

import csv
import os
from typing import Dict, List

CSV_PATH = os.path.join(os.path.dirname(__file__), "login_credentials.csv")


def load_login_credentials(path: str = CSV_PATH) -> List[Dict[str, str]]:
    """Loads every row of the login-credentials CSV as a list of dicts."""
    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)
