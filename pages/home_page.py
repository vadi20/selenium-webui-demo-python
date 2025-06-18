from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class HomePage(BasePage):
    # Locators
    LOGIN_MENU = (By.ID, "login2")
    LOGOUT_MENU = (By.ID, "logout2")
    SIGNUP_MENU = (By.ID, "signin2")
    WELCOME_MESSAGE = (By.ID, "nameofuser")
    CART_MENU = (By.ID, "cartur")
    HOME_MENU = (By.XPATH, "//a[contains(text(),'Home')]")
    CONTACT_MENU = (By.XPATH, "//a[contains(text(),'Contact')]")
    ABOUT_US_MENU = (By.XPATH, "//a[contains(text(),'About us')]")
    CATEGORIES_TITLE = (By.ID, "cat")
    PHONES_CATEGORY = (By.XPATH, "//a[contains(text(),'Phones')]")
    LAPTOPS_CATEGORY = (By.XPATH, "//a[contains(text(),'Laptops')]")
    MONITORS_CATEGORY = (By.XPATH, "//a[contains(text(),'Monitors')]")
    CAROUSEL_PREV = (By.CLASS_NAME, "carousel-control-prev")
    CAROUSEL_NEXT = (By.CLASS_NAME, "carousel-control-next")
    CAROUSEL_INDICATORS = (By.XPATH, "//li[contains(@data-target,'#carouselExampleIndicators')]")
    PRODUCT_CARD = (By.CLASS_NAME, "card-block")
    SELECT_DEFAULT_PRODUCT= (By.XPATH, "//a[@class='hrefch']")
    
    def navigate_to_home(self):
        self.driver.get(self.config.get('DEFAULT', 'base_url'))
        self.wait.until(EC.title_contains("STORE"))
    
    def click_login_menu(self):
        self.click(self.LOGIN_MENU)
    
    def click_logout_menu(self):
        self.click(self.LOGOUT_MENU)
    
    def click_signup_menu(self):
        self.click(self.SIGNUP_MENU)
    
    def click_cart_menu(self):
        self.click(self.CART_MENU)
    
    def get_welcome_message(self):
        return self.get_text(self.WELCOME_MESSAGE)
    
    def is_login_menu_displayed(self):
        return self.is_visible(self.LOGIN_MENU)

    def select_category(self, category_name):
        if category_name.lower() == "phones":
            self.click(self.PHONES_CATEGORY)
        elif category_name.lower() == "laptops":
            self.click(self.LAPTOPS_CATEGORY)
        elif category_name.lower() == "monitors":
            self.click(self.MONITORS_CATEGORY)
        else:
            raise ValueError(f"Unknown category: {category_name}")
        time.sleep(1) 
    
    def get_categories_title(self):
        return self.get_text(self.CATEGORIES_TITLE)
    
    def get_product_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_CARD))
    
    def navigate_carousel(self, direction="next"):
        if direction.lower() == "next":
            self.click(self.CAROUSEL_NEXT)
        elif direction.lower() == "prev":
            self.click(self.CAROUSEL_PREV)
        else:
            raise ValueError("Direction must be 'next' or 'prev'")
        time.sleep(1) 
            
    def get_active_carousel_item_index(self):
        indicators = self.driver.find_elements(*self.CAROUSEL_INDICATORS)
        for i, indicator in enumerate(indicators):
            if "active" in indicator.get_attribute("class"):
                return i
        return -1
    
    def select_default_product(self):
        self.click(self.SELECT_DEFAULT_PRODUCT)