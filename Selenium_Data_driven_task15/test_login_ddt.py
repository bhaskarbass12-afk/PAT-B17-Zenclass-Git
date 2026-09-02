import pytest
from excel_utils import ExcelManager

_excel = ExcelManager()
_login_rows = _excel.read_login_data()

@pytest.mark.parametrize("data", _login_rows, ids=[r["test_id"] for r in _login_rows])
def test_login_data_driven(login_page, excel, data):
    """
    Data-driven: one run per Excel row.
    Writes Date, Time and 'Test Passed'/'Test Failed' back to the sheet.
    """
    success = login_page.login(data["username"], data["password"])

    result_text = "Test Passed" if success else "Test Failed"
    excel.write_result(data["row"], result_text)

    # OrangeHRM: username is case-insensitive, password is case-sensitive.
    is_valid_pair = (
        str(data["username"]).strip().lower() == "admin"
        and str(data["password"]) == "admin123"
    )

    if is_valid_pair:
        assert success, f"{data['test_id']}: valid credentials should log in."
    else:
        assert not success, f"{data['test_id']}: invalid credentials should NOT log in."
