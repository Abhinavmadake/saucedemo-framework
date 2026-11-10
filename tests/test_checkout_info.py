import pytest

from pages.checkout_overview_page import CheckoutOverviewPage
from utils.data_loader import load_cases
from utils.logger import step


@pytest.mark.parametrize("case", load_cases("checkout_data.csv"))
def test_checkout_info_case(checkout_info_page, driver, case):
    """Runs once per row of testdata/checkout_data.csv."""
    tc = case["tc_id"]
    step(f"Enter {case['first_name']!r} / {case['last_name']!r} / {case['postal_code']!r}")
    checkout_info_page.fill(case["first_name"], case["last_name"], case["postal_code"])
    step("Click Continue")
    checkout_info_page.submit()

    if case["expected"].lower() == "valid":
        assert CheckoutOverviewPage(driver).is_open(), f"{tc}: Checkout: Overview should open"
    else:
        error = checkout_info_page.error_text()
        assert error, f"{tc}: a validation error should be displayed"
        assert case["expected_error"] in error, f"{tc}: expected {case['expected_error']!r} in {error!r}"
        assert checkout_info_page.is_open(), f"{tc}: user should remain on Checkout: Your Information"
