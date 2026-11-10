import pytest

from pages.checkout_overview_page import CheckoutOverviewPage
from utils.data_loader import load_cases, parse_items
from utils.logger import step


@pytest.mark.parametrize("case", load_cases("order_data.csv"))
def test_checkout_flow_case(inventory_page, driver, case):
    """Runs once per row of testdata/order_data.csv. stop_at is info, overview or complete."""
    tc = case["tc_id"]
    stop_at = case["stop_at"].lower()
    for name in parse_items(case["items"], inventory_page.product_names()):
        step(f"Click Add to cart for {name!r}")
        inventory_page.add_to_cart(name)

    step("Open the cart")
    cart = inventory_page.open_cart()
    assert cart.is_open(), f"{tc}: Your Cart page should open"
    step("Click Checkout")
    info = cart.checkout()
    assert info.is_open(), f"{tc}: Checkout: Your Information should open"
    assert info.title() == "Checkout: Your Information", f"{tc}: wrong page title"
    if stop_at == "info":
        return

    step(f"Fill in {case['first_name']!r} / {case['last_name']!r} / {case['postal_code']!r}")
    info.fill(case["first_name"], case["last_name"], case["postal_code"])
    step("Click Continue")
    info.submit()
    overview = CheckoutOverviewPage(driver)
    assert overview.is_open(), f"{tc}: Checkout: Overview should open"
    if stop_at == "overview":
        return

    step("Click Finish")
    complete = overview.finish()
    assert complete.is_open(), f"{tc}: Checkout: Complete! should open"
    assert complete.header_text() == "Thank you for your order!", f"{tc}: should show Thank you for your order!"
    assert complete.cart_badge_count() == 0, f"{tc}: cart badge should be gone after the order"
