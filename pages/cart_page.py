from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    CART_ITEMS = ( By.XPATH,"//tr[@class='success']/td[2]")#(By.XPATH, "//tbody/tr[@class='success']")
    ITEM_NAMES = (By.XPATH, "//tbody/tr/td[2]")
    ITEM_PRICES = (By.XPATH, "//tbody/tr/td[3]")
    DELETE_LINKS = (By.XPATH, "//a[contains(text(),'Delete')]")#"//tbody/tr/td[4]/a")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(),'Place Order')]")
    TOTAL_PRICE = (By.ID, "totalp")
    
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