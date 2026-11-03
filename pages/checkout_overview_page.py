from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.checkout_complete_page import CheckoutCompletePage


class CheckoutOverviewPage(BasePage):
    PATH = "checkout-step-two.html"
    TITLE_TEXT = "Checkout: Overview"
    FINISH = (By.CSS_SELECTOR, '[data-test="finish"]')

    def finish(self):
        self.click(self.FINISH)
        return CheckoutCompletePage(self.driver)
