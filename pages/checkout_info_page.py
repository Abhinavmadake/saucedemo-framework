from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    PATH = "checkout-step-one.html"
    TITLE_TEXT = "Checkout: Your Information"
    FIRST_NAME = (By.CSS_SELECTOR, '[data-test="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL_CODE = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    CONTINUE = (By.CSS_SELECTOR, '[data-test="continue"]')
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    def fill(self, first, last, postal):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)

    def submit(self):
        self.click(self.CONTINUE)

    def error_text(self):
        return self.optional_text(self.ERROR)
