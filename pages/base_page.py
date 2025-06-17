from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from utils.config import Config
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.logger = logging.getLogger(__name__)

    # Core Interaction Methods
    def click(self, locator):
        self.logger.info(f"Clicking on element: {locator}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        self.logger.info(f"Typing '{text}' in element: {locator}")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        self.logger.info(f"Getting text from element: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def wait_till_not_visible(self, locator, timeout=Config.EXPLICIT_WAIT):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    def is_displayed(self, locator, timeout=Config.EXPLICIT_WAIT):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
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

    # Navigation
    def get_current_url(self):
        return self.driver.current_url

    def refresh_page(self):
        self.driver.refresh()