from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import BASE_URL, TIMEOUT


class BasePage:
    PATH = ""
    TITLE_TEXT = ""
    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def open(self):
        self.driver.get(BASE_URL + self.PATH)
        return self

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def is_visible(self, locator, timeout=TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def optional_text(self, locator, timeout=3):
        return self.text_of(locator) if self.is_visible(locator, timeout) else ""

    def title(self):
        return self.text_of(self.TITLE)

    def is_open(self):
        try:
            self.wait.until(lambda d: d.find_element(*self.TITLE).text == self.TITLE_TEXT)
            return True
        except TimeoutException:
            return False
