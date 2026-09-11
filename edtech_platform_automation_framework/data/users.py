"""Test user data for the EdTech platform automation framework.

Valid credentials belong to a real GUVI account and must never be
hardcoded here - they're read from environment variables (GUVI_EMAIL /
GUVI_PASSWORD), populated via a local, git-ignored `.env` file (copy
`.env.example` at the project root to `.env` and fill in real values).

Invalid credentials are intentionally fake and don't correspond to a
real account, so they're safe to hardcode directly.
"""

import os

from dotenv import load_dotenv

# Loads GUVI_EMAIL / GUVI_PASSWORD from a local .env file if present.
# The .env file is git-ignored; never commit real credentials.
load_dotenv()

VALID_EMAIL = os.getenv("GUVI_EMAIL")
VALID_PASSWORD = os.getenv("GUVI_PASSWORD")

INVALID_EMAIL = "no_such_user_xyz123@example.com"
INVALID_PASSWORD = "WrongPassword123!"
