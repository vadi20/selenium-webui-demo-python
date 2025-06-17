from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutPage(BasePage):
    NAME_INPUT = (By.ID, "name")
    COUNTRY_INPUT = (By.ID, "country")
    CITY_INPUT = (By.ID, "city")
    CARD_INPUT = (By.ID, "card")
    MONTH_INPUT = (By.ID, "month")
    YEAR_INPUT = (By.ID, "year")
    PURCHASE_BTN = (By.XPATH, "//button[contains(text(),'Purchase')]")
    CONFIRMATION_MODAL = (By.XPATH, "//div[@class='sweet-alert']")
    CONFIRMATION_TEXT = (By.XPATH, "//div[contains(@class,'sweet-alert')]/h2")

    def fill_checkout_form(self, name, country, city, card, month, year):
        form_data = {
            self.NAME_INPUT: name,
            self.COUNTRY_INPUT: country,
            self.CITY_INPUT: city,
            self.CARD_INPUT: card,
            self.MONTH_INPUT: month,
            self.YEAR_INPUT: year
        }
        for locator, value in form_data.items():
            self.type(locator, value)

    def complete_purchase(self):
        self.click(self.PURCHASE_BTN)
        return self.get_confirmation_details()

    def get_confirmation_details(self):
        return {
            "message": self.get_text(self.CONFIRMATION_TEXT),
            "success": "Thank you" in self.get_text(self.CONFIRMATION_TEXT)
        }

    def get_confirmation_message(self):
        return self.get_text(self.CONFIRMATION_TEXT)
    
    def close_confirmation(self):
        ok_button = (By.XPATH, "//button[contains(text(),'OK')]")
        self.click(ok_button)