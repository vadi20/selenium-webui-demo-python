from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
import time

class CartPage(BasePage):
    CART_SUCCESS = ( By.XPATH,"//tr[@class='success']/td[2]")#(By.XPATH, "//tbody/tr[@class='success']")
    CART_ITEMS = (By.XPATH, "//tbody[@id='tbodyid']/tr")

    ITEM_NAMES = (By.XPATH, "//td[2]")
    ITEM_PRICES = (By.XPATH, "//td[3]")

    CART_LIST = (By.ID, "tbodyid")
    ITEM_NAME = (By.XPATH, "./td[2]")
    ITEM_PRICE = (By.XPATH, "./td[3]")

    DELETE_LINKS = (By.XPATH, "//a[contains(text(),'Delete')]")#"//tbody/tr/td[4]/a")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(),'Place Order')]")
    TOTAL_PRICE = (By.ID, "totalp")
    
    def get_cart_items_count(self):
        return len(self.driver.find_elements(*self.CART_SUCCESS))
    
    def get_item_details(self, index=0):
        items = self.driver.find_elements(*self.CART_SUCCESS)
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
    
    def validate_cart_contents(self, expected_items):
        actual_items = self.get_all_cart_items()
        self.logger.info(f"Acutal items  {str(actual_items)}")
        self.logger.info(f"Expected items {str(expected_items)}")

        expected_set = {(item['name'], float(item['price'])) for item in expected_items}
        actual_set = {(item['name'], item['price']) for item in actual_items}

        assert len(actual_set) == len(expected_set), f"Expected {len(expected_set)} items, found {len(actual_set)}"

        missing_items = expected_set - actual_set
        assert not missing_items, f"Missing items in cart: {missing_items}"
    
    
        extra_items = actual_set - expected_set
        assert not extra_items, f"Unexpected items in cart: {extra_items}"
        
        expected_total = sum(float(item['price']) for item in expected_items)
        actual_total = self.get_displayed_total()
        assert abs(expected_total - actual_total) < 0.01, f"Total price mismatch. Expected: {expected_total}, Actual: {actual_total}"
        
        self.logger.info("Cart validation passed for all items and total price")

    def get_all_cart_items(self):
        items = []
        #rows = self.driver.find_elements(*self.CART_ITEMS)
        self.wait.until(EC.presence_of_element_located(self.CART_LIST))
        rows =  self.driver.find_elements(*self.CART_ITEMS)

        self.logger.info(f"Found {len(rows)} items in cart")

        for row in rows:
            try:
                name = row.find_element(*self.ITEM_NAME).text
                price = float(row.find_element(*self.ITEM_PRICE).text)
                items.append({
                    "name": name,
                    "price": price
                })
                self.logger.debug(f"Added item to cart list: {name} - {price}")
            except Exception as e:
                self.logger.error(f"Error processing cart row: {str(e)}")
                continue

        self.logger.info(f"Found {len(items)} items in cart")
        return items

    def delete_all_items(self):
        delete_buttons = self.driver.find_elements(*self.DELETE_LINKS)
        if len(delete_buttons) > 0 :
            while delete_buttons:
                delete_buttons[0].click()
                self.wait.until(EC.staleness_of(delete_buttons[0]))
                delete_buttons = self.driver.find_elements(*self.DELETE_LINKS)
        self.logger.info("Deleted all items from cart")

    def get_displayed_total(self):
        total_text = self.wait.until(EC.visibility_of_element_located(self.TOTAL_PRICE)).text
        return float(total_text) if total_text else 0.0