from selenium.webdriver.common.by import By
from .base_page import BasePage

class ProductPage(BasePage):
    PRODUCT_NAME = (By.XPATH, "//h2[@class='name']")
    PRODUCT_PRICE = (By.XPATH, "//h3[@class='price-container']")
    PRODUCT_DESC = (By.XPATH, "//div[@id='more-information']/p")
    ADD_TO_CART_BTN = (By.XPATH, "//a[contains(text(),'Add to cart')]")

    def get_product_details(self):
        return {
            "name": self.get_text(self.PRODUCT_NAME),
            "price": self.get_text(self.PRODUCT_PRICE),
            "description": self.get_text(self.PRODUCT_DESC)
        }

    def get_product_name(self):
        return self.get_text(self.PRODUCT_NAME)
    
    def get_product_price(self):
        return self.get_text(self.PRODUCT_PRICE)
    
    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)
        return self.get_alert_text() 

    def navigate_back_to_home(self):
        from .home_page import HomePage
        self.driver.back()
        return HomePage(self.driver)