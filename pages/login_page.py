from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "loginusername")
    PASSWORD_FIELD = (By.ID, "loginpassword")
    LOGIN_MODAL_BUTTON = (By.ID, "login2")
    LOGIN_MODAL = (By.ID, "logInModal")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Log in')]")
    CLOSE_BUTTON = (By.XPATH, "//div[@id='logInModal']//button[text()='Close']")

    def open_login_modal(self):
        self.click(self.LOGIN_MODAL_BUTTON)
        self.is_displayed(self.LOGIN_MODAL)

    def close_modal(self):
        self.click(self.CLOSE_BUTTON)

    def enter_username(self, username):
        self.send_keys(self.USERNAME_FIELD, username)
    
    def enter_password(self, password):
        self.send_keys(self.PASSWORD_FIELD, password)
    
    def click_login(self):
        self.click(self.LOGIN_BUTTON)
    
    def close_login_modal(self):
        self.click(self.CLOSE_BUTTON)
    
    def login(self, username, password):
        #self.open_login_modal()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()