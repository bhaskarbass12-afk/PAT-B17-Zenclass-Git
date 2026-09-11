"""Static admin credentials and constants shared across the suite.

The bulk of the login test data lives in `login_credentials.csv` (the
"structured external data source" the brief asks for); this module just
holds the one set of admin credentials needed to drive the admin-only
flows (creating users, assigning leave).
"""

ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "admin123"

# A broad, single-letter search term for the "Employee Name" autocomplete
# fields on Add User / Assign Leave. This public demo's employee list is
# shared and can change over time, so a specific hardcoded employee name
# (even one previously confirmed to exist) can silently stop matching -
# a common letter reliably returns at least one real employee regardless
# of exactly who's currently in the demo data. The framework always picks
# the first non-placeholder suggestion returned (see
# BasePage.select_autocomplete_suggestion), so which employee it is
# doesn't matter for these tests.
EXISTING_EMPLOYEE_SEARCH_TEXT = "a"
