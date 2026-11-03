"""Checkout flow module: FR-11 (Checkout) and FR-16 (Complete Order).

Both are happy-path flows, so they run as smoke and regression.
"""

import pytest

from pages.checkout_overview_page import CheckoutOverviewPage
from utils.logger import step

ITEM = "Sauce Labs Backpack"
FIRST_NAME = "Test"
LAST_NAME = "User"
POSTAL_CODE = "12345"


@pytest.mark.smoke
@pytest.mark.regression
def test_fr11_checkout_opens_info_page(inventory_page):
    """TC-11-01"""
    step(f"Click Add to cart for {ITEM!r}")
    inventory_page.add_to_cart(ITEM)
    step("Open the cart")
    cart = inventory_page.open_cart()
    assert cart.is_open(), "FR-11: Your Cart page should open"
    step("Click Checkout")
    info = cart.checkout()
    assert info.is_open(), "FR-11: Checkout: Your Information should open"
    assert info.title() == "Checkout: Your Information", "FR-11: title should be Checkout: Your Information"


@pytest.mark.smoke
@pytest.mark.regression
def test_fr16_complete_order(checkout_info_page, driver):
    """TC-16-01"""
    step(f"Fill in {FIRST_NAME!r} / {LAST_NAME!r} / {POSTAL_CODE!r}")
    checkout_info_page.fill(FIRST_NAME, LAST_NAME, POSTAL_CODE)
    step("Click Continue")
    checkout_info_page.submit()
    overview = CheckoutOverviewPage(driver)
    assert overview.is_open(), "FR-16: Checkout: Overview should open"
    step("Click Finish")
    complete = overview.finish()
    assert complete.is_open(), "FR-16: Checkout: Complete! should open"
    assert complete.header_text() == "Thank you for your order!", "FR-16: should show Thank you for your order!"
    assert complete.cart_badge_count() == 0, "FR-16: cart badge should be gone after the order"
