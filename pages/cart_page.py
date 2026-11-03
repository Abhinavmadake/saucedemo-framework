from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.checkout_info_page import CheckoutInfoPage


class CartPage(BasePage):
    PATH = "cart.html"
    TITLE_TEXT = "Your Cart"
    ITEM = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    ITEM_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    ITEM_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    CHECKOUT = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def items(self):
        self.is_open()
        return [
            {"name": item.find_element(*self.ITEM_NAME).text, "price": item.find_element(*self.ITEM_PRICE).text}
            for item in self.driver.find_elements(*self.ITEM)
        ]

    def checkout(self):
        self.click(self.CHECKOUT)
        return CheckoutInfoPage(self.driver)
