import pytest

from pages.inventory_page import InventoryPage
from utils.config import PASSWORD, USERNAME
from utils.data_loader import load_csv
from utils.logger import step


@pytest.mark.smoke
@pytest.mark.regression
def test_fr01_login_success(login_page, driver):
    """TC-01-01"""
    step("Log in with valid credentials")
    login_page.login(USERNAME, PASSWORD)

    products_page = InventoryPage(driver)
    assert products_page.is_open(), "FR-01: Products page should open after successful login"
    assert products_page.title() == "Products", "FR-01: page title should be exactly Products"


@pytest.mark.regression
@pytest.mark.parametrize("row", load_csv("login_data.csv"), ids=lambda row: row["tc_id"])
def test_fr02_invalid_password(login_page, row):
    """TC-02-01, TC-02-02, TC-02-03, TC-02-04"""
    step(f"Log in with username {row['username']!r} and invalid password {row['password']!r}")
    login_page.login(row["username"], row["password"])

    assert row["expected_error"] in login_page.error_text(), (
        f"{row['tc_id']}: expected invalid-password error banner"
    )
    assert login_page.is_open(), f"{row['tc_id']}: user should remain on the Login page"


@pytest.mark.regression
def test_fr04_blank_password(login_page):
    """TC-04-01"""
    step("Log in with a valid username and an empty password")
    login_page.login(USERNAME, "")

    assert "Password is required" in login_page.error_text(), (
        "FR-04: error banner should contain Password is required"
    )
    assert login_page.is_open(), "FR-04: user should remain on the Login page"
