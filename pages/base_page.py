import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import BASE_URL, DEMO_DELAY, TIMEOUT


class BasePage:
    demo_mode = False
    PATH = ""
    TITLE_TEXT = ""
    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT, ignored_exceptions=(StaleElementReferenceException,))

    def pause(self):
        # Justified sleep: only with --demo, so a live audience can follow each action. Never used for synchronisation.
        if BasePage.demo_mode:
            time.sleep(DEMO_DELAY)

    def open(self):
        self.driver.get(BASE_URL + self.PATH)
        self.pause()
        return self

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        self.pause()

    def type(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)
        self.pause()

    def text_of(self, locator):
        return self.find(locator).text

    def is_visible(self, locator, timeout=TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout, ignored_exceptions=(StaleElementReferenceException,)).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def optional_text(self, locator, timeout=3):
        return self.text_of(locator) if self.is_visible(locator, timeout) else ""

    def title(self):
        return self.text_of(self.TITLE)

    def cart_badge_count(self):
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def is_open(self):
        try:
            self.wait.until(lambda d: d.find_element(*self.TITLE).text == self.TITLE_TEXT)
            return True
        except TimeoutException:
            return False
