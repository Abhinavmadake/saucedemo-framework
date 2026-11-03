from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    PATH = "checkout-complete.html"
    TITLE_TEXT = "Checkout: Complete!"
    HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')

    def header_text(self):
        return self.text_of(self.HEADER)
