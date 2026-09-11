"""Test-Case-9: Assign leave to an employee and verify assignment."""

from data.users import EXISTING_EMPLOYEE_SEARCH_TEXT
from pages.authenticated_page import AuthenticatedPage
from pages.leave_page import LeaveModulePage
from utils.logger import get_logger

logger = get_logger(__name__)


def test_assign_leave_to_employee(admin_login):
    """Logs in with an Admin user, navigates to Leave > Assign Leave,
    fills in the employee, leave type, and duration, submits the form,
    and verifies a success message confirming the assignment.
    """
    home_page = AuthenticatedPage(admin_login)
    home_page.click_menu_item("Leave")

    leave_module = LeaveModulePage(admin_login)
    assert leave_module.is_displayed(), "Expected to land on the Leave module"

    assign_leave_page = leave_module.open_assign_leave()
    assert assign_leave_page.is_displayed(), "Expected to reach the Assign Leave form"

    # This OrangeHRM instance's date fields are configured for a
    # yyyy-dd-mm format (confirmed via the input's own placeholder text
    # and its "Should be a valid date in yyyy-dd-mm format" validation
    # message) - day before month, not the more common yyyy-mm-dd.
    # These represent December 1, 2026 - December 2, 2026.
    leave_type = assign_leave_page.assign_leave(
        employee_search_text=EXISTING_EMPLOYEE_SEARCH_TEXT,
        from_date="2026-01-12",
        to_date="2026-02-12",
    )

    confirmation = assign_leave_page.get_confirmation()
    logger.info(
        "Leave assignment confirmation for '%s' (type=%s): %s",
        EXISTING_EMPLOYEE_SEARCH_TEXT,
        leave_type,
        confirmation,
    )
    assert confirmation, "Expected a success message confirming the leave assignment"
