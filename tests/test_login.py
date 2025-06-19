import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.logger import get_logger
from utils.json_reader import JSONReader

login_test_data = JSONReader.get_data("login_data.json", "login_test_cases")

@pytest.mark.login
@pytest.mark.regression

@pytest.mark.usefixtures("setup")
class TestLogin:

   # @pytest.fixture(params=JSONReader.get_data("login_data.json", "login_test_cases"))
   # def login_data(self, request):
   #     return request.param
    
    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.logger = get_logger(f"test.{self.__class__.__name__}")
        
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)
        
        self.home_page.navigate_to_home()
        self.home_page.click_login_menu()

    @pytest.mark.parametrize("login_data", login_test_data)
    def test_login_scenarios(self, login_data):
        self.logger.info(f"===== Testing: {login_data['test_name']} =====")
        
        
        self.login_page.enter_username(login_data["username"])
        self.login_page.enter_password(login_data["password"])
        self.login_page.click_login()
        
        if login_data["expected_result"] == "welcome_message":
            welcome_text = self.home_page.get_welcome_message()
            assert login_data["expected_text"] in welcome_text
        elif login_data["expected_result"] == "alert_message":
            alert_text = self.home_page.get_alert_text()
            assert login_data["expected_text"] in alert_text
        
        self.logger.info(f"Test '{login_data['test_name']}' passed")
    
    @pytest.mark.smoke    
    def test_logout(self):
        valid_data = [data for data in login_test_data if data.get("include_in_logout_test", False)]

        if not valid_data:
            pytest.skip("No valid login data found for logout testing")
        
        login_data = valid_data[0]
        self.logger.info("===== TESTING LOGOUT =====")
        
        self.login_page.login(login_data["username"], login_data["password"])
        self.home_page.click_logout_menu()
        
        assert self.home_page.is_login_menu_displayed()
        assert not self.home_page.is_visible(self.home_page.WELCOME_MESSAGE)

        self.logger.info("Logout test passed")