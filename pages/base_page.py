from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from utils.custom_waits import element_has_css_property
from utils.logger import get_logger
from utils.config_manager import app_config

from selenium.webdriver.common.by import By

class BasePage:

    def __init__(self, driver):
        self.config = app_config.config
        self.driver = driver
        self.timeout = self.config.get('DEFAULT', 'implicit_wait')
        self.wait = WebDriverWait(driver,  self.timeout)
        self.logger = get_logger(self.__class__.__name__)
     

    # Core Interaction Methods
    def click(self, locator):
        self.logger.info(f"Clicking on element: {locator}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def send_keys(self, locator, text):
        self.logger.info(f"Typing '{text}' in element: {locator}")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        self.logger.info(f"Getting text from element: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_not_visible(self, locator):
        self.logger.info(f"Checking non visibility of element: {locator}")
        WebDriverWait(self.driver, self.timeout).until(EC.invisibility_of_element_located(locator))

    def is_visible(self, locator):
        try:
            self.logger.info(f"Checking visibility of element: {locator}")
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # Advanced Interactions
    def hover(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        ActionChains(self.driver).move_to_element(element).perform()

    def press_key(self, locator, key):
        keys = {
            'enter': Keys.ENTER,
            'escape': Keys.ESCAPE
        }
        self.wait.until(EC.visibility_of_element_located(locator)).send_keys(keys[key.lower()])

    def get_alert_text(self):
        try:
            alert = self.wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except TimeoutException:
            raise NoSuchElementException("No alert present")
    
    def wait_for_css_property(self, locator, property_name, property_value):
        self.logger.info(f"Waiting for {property_name}={property_value} on element: {locator}")
        return self.wait.until(
            element_has_css_property(locator, property_name, property_value))
    
    def find_element_by_text(self, text, element_type='*'):
        return self.driver.find_element(By.XPATH, f"//{element_type}[contains(text(), '{text}')]")

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False