import pytest

from pages.inventory_page import InventoryPage
from utils.data_loader import load_cases
from utils.logger import step


@pytest.mark.parametrize("case", load_cases("login_data.csv"))
def test_login_case(login_page, driver, case):
    """Runs once per row of testdata/login_data.csv."""
    tc = case["tc_id"]
    step(f"Log in with username {case['username']!r} and password {case['password']!r}")
    login_page.login(case["username"], case["password"])

    if case["expected"].lower() == "valid":
        products_page = InventoryPage(driver)
        assert products_page.is_open(), f"{tc}: Products page should open after login"
        assert products_page.title() == "Products", f"{tc}: page title should be exactly Products"
    else:
        error = login_page.error_text()
        assert error, f"{tc}: an error banner should be displayed"
        assert case["expected_error"] in error, f"{tc}: expected {case['expected_error']!r} in {error!r}"
        assert login_page.is_open(), f"{tc}: user should remain on the Login page"
