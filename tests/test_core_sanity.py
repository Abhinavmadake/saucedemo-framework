from pages.checkout_overview_page import CheckoutOverviewPage
from utils.logger import step


def test_core_sanity(checkout_info_page, driver):
    """Setup check for the framework core. Delete before final submission."""
    step("Fill checkout information")
    checkout_info_page.fill("Test", "User", "12345")
    step("Click Continue")
    checkout_info_page.submit()
    overview = CheckoutOverviewPage(driver)
    assert overview.is_open(), "Checkout: Overview should open"
    step("Click Finish")
    complete = overview.finish()
    assert complete.is_open(), "Checkout: Complete! should open"
    assert complete.header_text() == "Thank you for your order!"
