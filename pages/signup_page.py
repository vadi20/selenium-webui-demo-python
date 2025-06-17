from selenium.webdriver.common.by import By
from .base_page import BasePage

class SignupPage(BasePage):
    SIGNUP_USERNAME = (By.ID, "sign-username")
    SIGNUP_PASSWORD = (By.ID, "sign-password")
    SIGNUP_BUTTON = (By.XPATH, "//button[text()='Sign up']")

    def enter_signup_username(self, username):
        self.type(self.SIGNUP_USERNAME, username)

    def enter_signup_password(self, password):
        self.type(self.SIGNUP_PASSWORD, password)

    def click_signup(self):
        self.click(self.SIGNUP_BUTTON)

    def signup(self, username, password):
        self.enter_signup_username(username)
        self.enter_signup_password(password)
        self.click_signup()