import pytest
from selenium.webdriver.common.by import By
from utils.driver_manager import DriverManager
from configparser import ConfigParser
from utils.logger import get_logger, setup_logging
import time

setup_logging()
logger = get_logger(__name__)

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser to execute tests (chrome or firefox)"
    )
    parser.addoption(
        "--headless", action="store_true", help="run tests in headless mode"
    )

@pytest.fixture(scope="session")
def config():
    config = ConfigParser()
    config.read('config/config.ini')
    return config

@pytest.fixture(scope="session")
def browser_config(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    return {
        "browser": browser,
        "headless": headless
    }

@pytest.fixture(scope="function")
def setup(request, config, browser_config):
    logger.info("===== Setting up test fixture =====")
    
    driver = DriverManager.get_driver()
    
    request.cls.driver = driver
    request.cls.config = config
    
    if not browser_config["headless"]:
        driver.maximize_window()
    
    base_url = config.get('DEFAULT', 'base_url')
    driver.get(base_url)
    
    yield driver
    
    logger.info("===== Tearing down test fixture =====")
    if request.node.rep_call.failed:
        screenshot_name = f"screenshots/failure_{request.node.name}_{time.strftime('%Y%m%d_%H%M%S')}.png"
        try:
            driver.save_screenshot(screenshot_name)
            logger.info(f"Screenshot saved as {screenshot_name}")
        except:
            logger.error("Failed to save screenshot")
    
    #driver_manager.quit_driver()
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="function")
def login(setup, config):
    logger.info("===== Performing login =====")
    from pages.home_page import HomePage
    from pages.login_page import LoginPage
    
    home_page = HomePage(setup)
    login_page = LoginPage(setup)
    
    username = config.get('CREDENTIALS', 'valid_username')
    password = config.get('CREDENTIALS', 'valid_password')
    
    home_page.navigate_to_home()
    home_page.click_login_menu()
    login_page.login(username, password)
    
    yield
    
    logger.info("===== Performing logout =====")
    home_page.click_logout_menu()

@pytest.fixture(scope="function")
def product_in_cart(setup):
    logger.info("===== Adding product to cart =====")
    from pages.home_page import HomePage
    from pages.product_page import ProductPage
    
    home_page = HomePage(setup)
    product_page = ProductPage(setup)
    
    home_page.navigate_to_home()
    home_page.select_category("Phones")
    home_page.select_default_product()
    product_page.add_to_cart()
    home_page.get_alert_text() 
    
    yield
    
    logger.info("===== Cleaning up cart =====")
    home_page.click_cart_menu()
    from pages.cart_page import CartPage
    cart_page = CartPage(setup)
    while cart_page.get_cart_items_count() > 0:
        cart_page.delete_item(0)
        time.sleep(0.5)

def pytest_configure(config):
    import os
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    config.addinivalue_line(
        "markers", "smoke: smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: regression test"
    )
    config.addinivalue_line(
        "markers", "wip:  work in progress"
    )

    config.addinivalue_line(
        "markers", "login:  tests related to login functionality"
    )

def pytest_collection_modifyitems(config, items):
    skip_slow = pytest.mark.skip(reason="slow test")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)