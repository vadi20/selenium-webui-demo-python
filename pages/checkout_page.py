from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutPage(BasePage):
    NAME_FIELD = (By.ID, "name")
    COUNTRY_FIELD = (By.ID, "country")
    CITY_FIELD = (By.ID, "city")
    CREDIT_CARD_FIELD = (By.ID, "card")
    MONTH_FIELD = (By.ID, "month")
    YEAR_FIELD = (By.ID, "year")
    PURCHASE_BUTTON = (By.XPATH, "//button[contains(text(),'Purchase')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(),'Cancel')]")
    ORDER_CONFIRMATION = (By.CLASS_NAME, "sweet-alert")
    ORDER_DETAILS = (By.XPATH, "//p[@class='lead text-muted ']")
    
    def enter_name(self, name):
        self.send_keys(self.NAME_FIELD, name)
    
    def enter_country(self, country):
        self.send_keys(self.COUNTRY_FIELD, country)
    
    def enter_city(self, city):
        self.send_keys(self.CITY_FIELD, city)
    
    def enter_credit_card(self, card_number):
        self.send_keys(self.CREDIT_CARD_FIELD, card_number)
    
    def enter_month(self, month):
        self.send_keys(self.MONTH_FIELD, month)
    
    def enter_year(self, year):
        self.send_keys(self.YEAR_FIELD, year)
    
    def click_purchase(self):
        self.click(self.PURCHASE_BUTTON)
    
    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)
        
    def fill_order_form(self, name, country, city, card, month, year):
        self.enter_name(name)
        self.enter_country(country)
        self.enter_city(city)
        self.enter_credit_card(card)
        self.enter_month(month)
        self.enter_year(year)
    
    def get_order_confirmation_text(self):
        return self.get_text(self.ORDER_CONFIRMATION)
    
    def get_order_details(self):
        details_text = self.get_text(self.ORDER_DETAILS)
        details = {}
        for line in details_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                details[key.strip()] = value.strip()
        return details