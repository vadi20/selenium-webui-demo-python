import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.driver_manager import DriverManager
from utils.config import Config

@pytest.fixture
def setup():
    driver = DriverManager.get_driver()
    yield driver
    driver.quit()

def test_valid_login(setup):
    driver = setup
    home_page = HomePage(driver)
    login_page = LoginPage(driver)

    home_page.open_login_modal()
    login_page.login(Config.USERNAME, Config.PASSWORD)
    assert home_page.is_displayed(home_page.WELCOME_USER)
