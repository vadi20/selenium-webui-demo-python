from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "loginusername")
    PASSWORD_INPUT = (By.ID, "loginpassword")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Log in')]")
    CLOSE_BUTTON = (By.XPATH, "//div[@id='logInModal']//button[text()='Close']")

    def enter_credentials(self, username, password):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)

    def submit_login(self):
        self.click(self.LOGIN_BUTTON)

    def close_modal(self):
        self.click(self.CLOSE_BUTTON)

    def login(self, username, password):
        self.enter_credentials(username, password)
        self.submit_login()
