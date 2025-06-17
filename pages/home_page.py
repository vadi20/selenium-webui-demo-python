from selenium.webdriver.common.by import By
from .base_page import BasePage
from .login_page import LoginPage
from .product_page import ProductPage
from .cart_page import CartPage
from utils.config import Config

class HomePage(BasePage):
    # Locators
    LOGIN_LINK = (By.ID, "login2")
    SIGNUP_LINK = (By.ID, "signin2")
    LOGOUT_LINK = (By.ID, "logout2")
    WELCOME_USER = (By.ID, "nameofuser")
    CART_LINK = (By.ID, "cartur")
    CONTACT_LINK = (By.XPATH, "//a[contains(text(),'Contact')]")
    ABOUT_LINK = (By.XPATH, "//a[contains(text(),'About us')]")
    HOME_LINK = (By.XPATH, "//a[contains(text(),'Home')]")
    
    # Category Locators
    CATEGORIES = {
        "phones": (By.XPATH, "//a[contains(text(),'Phones')]"),
        "laptops": (By.XPATH, "//a[contains(text(),'Laptops')]"),
        "monitors": (By.XPATH, "//a[contains(text(),'Monitors')]")
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(Config.BASE_URL)

    # Core Actions
    def navigate_to_home(self):
        self.click(self.HOME_LINK)

    def open_login_modal(self):
        self.click(self.LOGIN_LINK)
        return LoginPage(self.driver)
    
    def go_to_cart(self):
        self.click(self.CART_LINK)
        return CartPage(self.driver)

    '''
    def open_signup_modal(self):
        self.click(self.SIGNUP_LINK)
        return SignupPage(self.driver)
    '''
    def navigate_to_category(self, category_name):
        category = category_name.lower()
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category_name}")
        self.click(self.CATEGORIES[category])

    def select_product(self, product_name):
        product_locator = (By.XPATH, f"//a[contains(text(),'{product_name}')]")
        self.click(product_locator)
        return ProductPage(self.driver)

    # Verification Methods
    def is_user_logged_in(self):
        return self.is_displayed(self.WELCOME_USER)

    def get_welcome_text(self):
        return self.get_text(self.WELCOME_USER) if self.is_user_logged_in() else ""