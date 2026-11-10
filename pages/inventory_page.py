from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.login_page import LoginPage


class InventoryPage(BasePage):
    PATH = "inventory.html"
    TITLE_TEXT = "Products"
    ITEM = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    ITEM_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    ITEM_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.CSS_SELECTOR, '[data-test="logout-sidebar-link"]')

    def _item(self, name):
        xpath = f'//*[@data-test="inventory-item"][.//*[@data-test="inventory-item-name" and normalize-space()="{name}"]]'
        return self.find((By.XPATH, xpath))

    def _button(self, name):
        return self._item(name).find_element(By.TAG_NAME, "button")

    def _press_and_wait(self, name, from_text, to_text):
        button = self._button(name)
        if button.text == from_text:
            button.click()
        self.wait.until(lambda d: self._button(name).text == to_text)
        self.pause()

    def product_names(self):
        self.find(self.ITEM)
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAME)]

    def product_price(self, name):
        return self._item(name).find_element(*self.ITEM_PRICE).text

    def add_to_cart(self, name):
        self._press_and_wait(name, "Add to cart", "Remove")

    def remove_from_cart(self, name):
        self._press_and_wait(name, "Remove", "Add to cart")

    def button_text(self, name):
        return self._button(name).text

    def open_cart(self):
        self.click(self.CART_LINK)
        return CartPage(self.driver)

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        return LoginPage(self.driver)
