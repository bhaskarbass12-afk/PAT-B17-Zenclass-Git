"""Test-Case-10: Initiate a claim request."""

from pages.authenticated_page import AuthenticatedPage
from pages.claim_page import ClaimModulePage
from utils.logger import get_logger

logger = get_logger(__name__)


def test_initiate_claim_request(admin_login):
    """Navigates to the Claim section, initiates a new claim by
    selecting a claim type (Event), entering an amount (as an expense
    line item, where available), and a reason (Remarks), submits the
    request, and verifies a confirmation message is displayed.

    See claim_page.py's module docstring for how this maps onto
    OrangeHRM's actual two-step "create claim, then add expense" flow.
    """
    home_page = AuthenticatedPage(admin_login)
    home_page.click_menu_item("Claim")

    claim_module = ClaimModulePage(admin_login)
    assert claim_module.is_displayed(), "Expected to land on the Claim module"

    submit_claim_page = claim_module.open_submit_claim()
    claim_type = submit_claim_page.create_claim(remarks="Automated test claim submission")

    confirmation = submit_claim_page.get_confirmation()
    logger.info("Claim creation confirmation (claim type=%s): %s", claim_type, confirmation)
    assert confirmation, "Expected a confirmation message after creating the claim"

    submit_claim_page.add_expense(amount="100")
    submit_claim_page.submit_for_approval()
