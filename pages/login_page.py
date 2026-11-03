from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, '[data-test="username"]')
    PASSWORD = (By.CSS_SELECTOR, '[data-test="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-test="login-button"]')
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')
    LOGO = (By.CSS_SELECTOR, ".login_logo")

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def error_text(self):
        return self.optional_text(self.ERROR)

    def title(self):
        return self.text_of(self.LOGO)

    def is_open(self):
        return self.is_visible(self.LOGIN_BUTTON)
