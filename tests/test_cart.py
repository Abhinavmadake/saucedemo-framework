import pytest

from utils.data_loader import load_cases, parse_items
from utils.logger import step


@pytest.mark.parametrize("case", load_cases("cart_data.csv"))
def test_cart_case(inventory_page, case):
    """Runs once per row of testdata/cart_data.csv."""
    tc = case["tc_id"]
    all_items = inventory_page.product_names()
    items = parse_items(case["items"], all_items)
    assert inventory_page.cart_badge_count() == 0, f"{tc}: cart badge should start empty"

    expected = []
    for count, name in enumerate(items, start=1):
        step(f"Note the price of {name!r} on Products, then click Add to cart")
        expected.append({"name": name, "price": inventory_page.product_price(name)})
        inventory_page.add_to_cart(name)
        assert inventory_page.cart_badge_count() == count, f"{tc}: badge should be {count} after adding {name!r}"
        assert inventory_page.button_text(name) == "Remove", f"{tc}: {name!r} button should change to Remove"

    for name in all_items:
        if name not in items:
            assert inventory_page.button_text(name) == "Add to cart", f"{tc}: {name!r} button should not change"

    step("Open the cart")
    cart = inventory_page.open_cart()
    assert cart.is_open(), f"{tc}: Your Cart page should open"
    in_cart = cart.items()
    assert sorted(in_cart, key=lambda i: i["name"]) == sorted(expected, key=lambda i: i["name"]), (
        f"{tc}: cart {in_cart} should match Products page {expected}"
    )
