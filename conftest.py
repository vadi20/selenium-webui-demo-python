import pytest
from selenium.webdriver import Chrome, Firefox
from utils.driver_manager import DriverManager
from utils.config import Config
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def config():
    """Provides access to test configuration"""
    return Config

@pytest.fixture(scope="function")
def browser(request):
    """Main browser fixture with automatic cleanup"""
    driver = None
    try:
        driver = DriverManager.get_driver()
        driver.maximize_window()
        logger.info(f"Initialized {Config.BROWSER} browser")
        yield driver
    finally:
        if driver:
            driver.quit()
            logger.info("Browser session terminated")

# --------------------------
# PAGE OBJECT FIXTURES
# --------------------------

@pytest.fixture
def home_page(browser):
    """Provides HomePage instance with automatic navigation"""
    page = HomePage(browser)
    page.navigate_to_home()
    return page

@pytest.fixture
def login_page(browser, home_page):
    """Provides LoginPage instance with modal already opened"""
    home_page.open_login_modal()
    return LoginPage(browser)

@pytest.fixture
def signup_page(browser, home_page):
    """Provides SignupPage instance with modal already opened"""
    home_page.open_signup_modal()
    return SignupPage(browser)

@pytest.fixture
def product_page(browser, home_page):
    """Provides ProductPage instance after selecting a product"""
    home_page.select_product("Samsung galaxy s6")
    return ProductPage(browser)

@pytest.fixture
def cart_page(browser, home_page):
    """Provides CartPage instance with empty cart"""
    page = CartPage(browser)
    page.driver.get(f"{Config.BASE_URL}cart.html")
    # Clear cart if needed
    delete_buttons = page.driver.find_elements(*page.DELETE_LINKS)
    for button in delete_buttons:
        button.click()
    return page

@pytest.fixture
def populated_cart(browser, home_page, cart_page):
    """Provides CartPage with test items already added"""
    home_page.select_product("Samsung galaxy s6")
    ProductPage(browser).add_to_cart()
    home_page.navigate_to_home()
    home_page.select_product("Nexus 6")
    ProductPage(browser).add_to_cart()
    return CartPage(browser)

@pytest.fixture
def checkout_page(browser, populated_cart):
    """Provides CheckoutPage instance with order ready"""
    populated_cart.place_order()
    return CheckoutPage(browser)


# --------------------------
# TEST DATA FIXTURES
# --------------------------

@pytest.fixture(params=[
    {"username": "valid_user", "password": "ValidPass123", "valid": True},
    {"username": "invalid", "password": "wrong", "valid": False}
])
def user_credentials(request):
    """Provides parameterized user credentials"""
    return request.param

@pytest.fixture
def test_products():
    """Provides test product data"""
    return [
        {"name": "Samsung galaxy s6", "category": "Phones"},
        {"name": "Nexus 6", "category": "Phones"},
        {"name": "MacBook air", "category": "Laptops"}
    ]

# --------------------------
# HOOKS
# --------------------------

def pytest_exception_interact(node, call, report):
    """Automatically capture screenshots on test failure"""
    if report.failed and "browser" in node.funcargs:
        browser = node.funcargs["browser"]
        try:
            browser.save_screenshot(f"reports/screenshots/{node.name}_failure.png")
            logger.error(f"Screenshot saved for failed test: {node.name}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")

@pytest.fixture(autouse=True)
def log_test_execution(request):
    """Automatic test execution logging"""
    logger.info(f"Starting test: {request.node.name}")
    yield
    logger.info(f"Completed test: {request.node.name}")