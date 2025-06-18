from selenium.webdriver.common.by import By
from .base_page import BasePage
#from utils.config import Config

class CartPage(BasePage):
    CART_ITEMS = ( By.XPATH,"//tr[@class='success']/td[2]")#(By.XPATH, "//tbody/tr[@class='success']")
    ITEM_NAMES = (By.XPATH, "//tbody/tr/td[2]")
    ITEM_PRICES = (By.XPATH, "//tbody/tr/td[3]")
    DELETE_LINKS = (By.XPATH, "//a[contains(text(),'Delete')]")#"//tbody/tr/td[4]/a")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(),'Place Order')]")
    TOTAL_PRICE = (By.ID, "totalp")

    '''def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(f"{Config.BASE_URL}cart.html")

    def get_cart_items(self):
        return {
            "count": len(self.driver.find_elements(*self.CART_ITEMS)),
            "names": [elem.text for elem in self.driver.find_elements(*self.ITEM_NAMES)],
            "prices": [elem.text for elem in self.driver.find_elements(*self.ITEM_PRICES)]
        }

    def delete_item(self, index=0):
        delete_buttons = self.driver.find_elements(*self.DELETE_LINKS)
        if index < len(delete_buttons):
            delete_buttons[index].click()
            self.wait_till_not_visible(delete_buttons[index])

    def place_order(self):
        from .checkout_page import CheckoutPage
        self.click(self.PLACE_ORDER_BTN)
        return CheckoutPage(self.driver)

    def get_total_price(self):
        return self.get_text(self.TOTAL_PRICE)'''
    
    def get_cart_items_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))
    
    def get_item_details(self, index=0):
        items = self.driver.find_elements(*self.CART_ITEMS)
        if index >= len(items):
            return None
        
        return {
            "name": items[index].find_element(*self.ITEM_NAME).text,
            "price": items[index].find_element(*self.ITEM_PRICE).text
        }
    
    def delete_item(self, index=0):
        delete_buttons = self.driver.find_elements(*self.DELETE_LINKS)
        if index < len(delete_buttons):
            delete_buttons[index].click()
    
    def get_total_price(self):
        return float(self.get_text(self.TOTAL_PRICE))
    
    def click_place_order(self):
        self.click(self.PLACE_ORDER_BUTTON)
    
    def is_cart_empty(self):
        return self.get_text(By.XPATH("//h2[contains(text(),'Products')]")) == "Products"