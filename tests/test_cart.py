"""Cart module: FR-07 (Add to Cart) and FR-09 (Cart Details).

Test design (EP + BVA on the number of items in the cart):
  EP:  every product is in the same class ("any item" in FR-07), so one
       representative item stands for the class; the item next to it is the
       control that must NOT change.
  BVA: cart size 0 -> 1 (lower edge, also the smoke case), 1 -> 2 (just above), 5 -> 6 (upper edge:
       SauceDemo lists 6 products, so 6 is the most the cart can hold).
"""

import pytest

from utils.logger import step

FIRST_ITEM = "Sauce Labs Backpack"
SECOND_ITEM = "Sauce Labs Bike Light"


@pytest.mark.smoke
@pytest.mark.regression
def test_fr07_add_one_item(inventory_page):
    """TC-07-01"""
    assert inventory_page.cart_badge_count() == 0, "FR-07: cart badge should start empty"
    step(f"Click Add to cart for {FIRST_ITEM!r}")
    inventory_page.add_to_cart(FIRST_ITEM)
    assert inventory_page.cart_badge_count() == 1, "FR-07: badge should go from 0 to 1"
    assert inventory_page.button_text(FIRST_ITEM) == "Remove", "FR-07: button should change to Remove"
    assert inventory_page.button_text(SECOND_ITEM) == "Add to cart", (
        "FR-07: only the clicked item's button should change"
    )


@pytest.mark.regression
def test_fr07_add_second_item(inventory_page):
    """TC-07-02"""
    step(f"Click Add to cart for {FIRST_ITEM!r}")
    inventory_page.add_to_cart(FIRST_ITEM)
    assert inventory_page.cart_badge_count() == 1, "FR-07: badge should be 1 after the first item"
    step(f"Click Add to cart for {SECOND_ITEM!r}")
    inventory_page.add_to_cart(SECOND_ITEM)
    assert inventory_page.cart_badge_count() == 2, "FR-07: badge should go from 1 to 2"
    assert inventory_page.button_text(SECOND_ITEM) == "Remove", "FR-07: second button should change to Remove"
    assert inventory_page.button_text(FIRST_ITEM) == "Remove", "FR-07: first button should stay Remove"


@pytest.mark.regression
def test_fr07_add_all_items(inventory_page):
    """TC-07-03"""
    names = inventory_page.product_names()
    for count, name in enumerate(names, start=1):
        step(f"Click Add to cart for {name!r}")
        inventory_page.add_to_cart(name)
        assert inventory_page.cart_badge_count() == count, f"FR-07: badge should be {count} after adding {name!r}"
        assert inventory_page.button_text(name) == "Remove", f"FR-07: {name!r} button should change to Remove"


@pytest.mark.smoke
@pytest.mark.regression
def test_fr09_cart_matches_products(inventory_page):
    """TC-09-01"""
    expected = []
    for name in (FIRST_ITEM, SECOND_ITEM):
        step(f"Note the price of {name!r} on Products, then click Add to cart")
        expected.append({"name": name, "price": inventory_page.product_price(name)})
        inventory_page.add_to_cart(name)
    step("Open the cart")
    cart = inventory_page.open_cart()
    assert cart.is_open(), "FR-09: Your Cart page should open"
    items = cart.items()
    assert len(items) == 2, f"FR-09: cart should list exactly 2 items, got {len(items)}"
    assert sorted(items, key=lambda i: i["name"]) == sorted(expected, key=lambda i: i["name"]), (
        f"FR-09: cart {items} should match Products page {expected}"
    )


@pytest.mark.regression
def test_fr09_cart_matches_all_products(inventory_page):
    """TC-09-02"""
    expected = []
    for name in inventory_page.product_names():
        step(f"Note the price of {name!r} on Products, then click Add to cart")
        expected.append({"name": name, "price": inventory_page.product_price(name)})
        inventory_page.add_to_cart(name)
    step("Open the cart")
    cart = inventory_page.open_cart()
    assert cart.is_open(), "FR-09: Your Cart page should open"
    items = cart.items()
    assert len(items) == len(expected), f"FR-09: cart should list {len(expected)} items, got {len(items)}"
    assert sorted(items, key=lambda i: i["name"]) == sorted(expected, key=lambda i: i["name"]), (
        f"FR-09: cart {items} should match Products page {expected}"
    )
