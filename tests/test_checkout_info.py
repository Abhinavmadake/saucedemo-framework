import pytest

from pages.checkout_overview_page import CheckoutOverviewPage
from utils.data_loader import load_csv
from utils.logger import step


@pytest.mark.regression
def test_fr12_first_name_required(checkout_info_page):
    """TC-12-01: Reject checkout information with a blank first name."""
    step("Leave First Name blank and enter valid last name and postal code")
    checkout_info_page.fill("", "User", "12345")
    step("Submit checkout information")
    checkout_info_page.submit()

    error = checkout_info_page.error_text()
    assert "First Name is required" in error, "FR-12 / TC-12-01: expected the required First Name error"
    assert checkout_info_page.is_open(), "FR-12 / TC-12-01: user should remain on Checkout: Your Information"


@pytest.mark.parametrize("case", load_csv("postal_codes.csv"), ids=lambda case: case["tc_id"])
@pytest.mark.regression
def test_fr14_postal_code_validation(checkout_info_page, driver, case):
    """TC-14-01 through TC-14-05: Validate postal code boundaries and equivalence classes."""
    step(f"Enter postal code {case['postal_code']} for {case['tc_id']}")
    checkout_info_page.fill("Test", "User", case["postal_code"])
    step("Submit checkout information")
    checkout_info_page.submit()

    if case["expected"] == "valid":
        overview = CheckoutOverviewPage(driver)
        assert overview.is_open(), f"FR-14 / {case['tc_id']}: valid postal code should open Checkout: Overview"
    else:
        error = checkout_info_page.error_text()
        assert error, f"FR-14 / {case['tc_id']}: invalid postal code should display a validation error"
        assert checkout_info_page.is_open(), (
            f"FR-14 / {case['tc_id']}: invalid postal code should remain on Checkout: Your Information"
        )
