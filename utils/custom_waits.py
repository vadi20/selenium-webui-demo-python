from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

class element_has_css_property(object):
    def __init__(self, locator, property_name, property_value):
        self.locator = locator
        self.property_name = property_name
        self.property_value = property_value
    
    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if isinstance(element, WebElement):
            return self.property_value in element.value_of_css_property(self.property_name)
        return False

class text_to_be_present_in_element_attribute(object):
    def __init__(self, locator, attribute, text):
        self.locator = locator
        self.attribute = attribute
        self.text = text
    
    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if isinstance(element, WebElement):
            return self.text in element.get_attribute(self.attribute)
        return False