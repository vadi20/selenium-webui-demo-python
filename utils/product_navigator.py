from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger
from utils.config_manager import app_config

import time

class ProductNavigator:
    def __init__(self, driver):
        self.config = app_config.config
        self.driver = driver
        self.timeout = self.config.get('PRODUCT_NAVIGATION', 'implicit_wait')
        self.max_pages = self.config.getint('PRODUCT_NAVIGATION', 'max_pages')

        self.wait = WebDriverWait(driver,  self.timeout)
        self.logger = get_logger(self.__class__.__name__)
        self.NEXT_BUTTON = (By.ID, "next2")
        self.PREV_BUTTON = (By.ID, "prev2")
        self.PRODUCT_NAMES = (By.XPATH, "//h4[@class='card-title']/a")
        self.PRODUCT_CARDS = (By.CLASS_NAME, "card-block")
        self.PAGE_INDICATOR = (By.CSS_SELECTOR, "#tbodyid")

    def find_and_select_product(self, product_name):
        self.logger.info(f"Searching for product: {product_name}")
        
        current_page = 1
        while current_page <= self.max_pages:
            self.logger.info(f"Checking page {current_page}")
            
            self._wait_for_page_load()

            products = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_NAMES))

            for product in products:
                if product_name.lower() in product.text.lower():
                    self.logger.info(f"Found product: {product.text}")
                    product.click()
                    self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "description")))
                    return True
            
            if self._go_to_next_page():
                current_page += 1
            else:
                break
        
        self.logger.warning(f"Product '{product_name}' not found in {self.max_pages} pages")
        return False

    def _go_to_next_page(self):
        try:
            next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON))
            if "disabled" not in next_button.get_attribute("class"):
                #current_page_marker = self.driver.find_element(*self.PAGE_INDICATOR)

                next_button.click()
                #self.wait.until(EC.staleness_of(current_page_marker))
                return True
            return False
        except (NoSuchElementException, TimeoutException) as e:
            return False
        
    def _wait_for_page_load(self):
        try:
            self.wait.until(EC.staleness_of(self.driver.find_element(*self.PAGE_INDICATOR)))
            self.wait.until(EC.presence_of_element_located(self.PRODUCT_NAMES))
        except TimeoutException:
            self.logger.warning("Page load wait timed out, proceeding anyway")
            pass