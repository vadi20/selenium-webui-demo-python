import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.driver_manager import DriverManager
from utils.logger import get_logger
from configparser import ConfigParser

@pytest.mark.usefixtures("setup")

class TestLogin:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.logger = get_logger(f"test.{self.__class__.__name__}")

        self.valid_username = self.config.get('CREDENTIALS', 'valid_username')
        self.valid_password = self.config.get('CREDENTIALS', 'valid_password')
        self.invalid_username = self.config.get('CREDENTIALS', 'invalid_username')
        self.invalid_password = self.config.get('CREDENTIALS', 'invalid_password')
        
        self.home_page = HomePage(self.driver,self.config)
        self.login_page = LoginPage(self.driver,self.config)
    
    def test_valid_login(self):
        self.logger.info("===== TESTING VALID LOGIN =====")
        self.home_page.navigate_to_home()
        self.home_page.click_login_menu()
        
        self.login_page.enter_username(self.valid_username)
        self.login_page.enter_password(self.valid_password)
        self.login_page.click_login()
        
        welcome_text = self.home_page.get_welcome_message()
        assert f"Welcome {self.valid_username}" in welcome_text
        self.logger.info("Valid login test passed")
    
    def test_invalid_login(self):
        self.logger.info("===== TESTING INVALID LOGIN =====")
        self.home_page.navigate_to_home()
        self.home_page.click_login_menu()
        
        self.login_page.enter_username(self.invalid_username)
        self.login_page.enter_password(self.invalid_password)
        self.login_page.click_login()
        
        alert_text = self.home_page.get_alert_text()
        assert "Wrong password" in alert_text or "User does not exist" in alert_text
        self.logger.info("Invalid login test passed")
    
    def test_logout(self):
        self.logger.info("===== TESTING LOGOUT =====")
        self.home_page.navigate_to_home()
        self.home_page.click_login_menu()
        
        self.login_page.login(self.valid_username, self.valid_password)
        self.home_page.click_logout_menu()
        
        assert self.home_page.is_login_menu_displayed()
        self.logger.info("Logout test passed")