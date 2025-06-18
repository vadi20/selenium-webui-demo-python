import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import get_logger


@pytest.mark.usefixtures("setup")
class TestOrder:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.logger = get_logger(f"test.{self.__class__.__name__}")

        self.home_page = HomePage(self.driver,self.config)
        self.product_page = ProductPage(self.driver,self.config)
        self.cart_page = CartPage(self.driver,self.config)
        self.order_page = CheckoutPage(self.driver,self.config)
        
        # Add a product to cart and go to order page
        self.home_page.navigate_to_home()
        self.home_page.select_category("Phones")
        self.home_page.select_default_product()
        self.product_page.add_to_cart()
        self.home_page.click_cart_menu()
        self.cart_page.click_place_order()
    
    def test_order_form_validation(self):
        self.logger.info("===== TESTING ORDER FORM VALIDATION =====")
        # Try to submit empty form
        self.order_page.click_purchase()
        alert_text = self.home_page.get_alert_text()
        assert "Please fill out Name and Creditcard" in alert_text
        
        self.logger.info("Order form validation test passed")
    
    def test_successful_order_confirmation(self):
        self.logger.info("===== TESTING SUCCESSFUL ORDER CONFIRMATION =====")
        test_data = {
            "name": "Test User",
            "country": "Test Country",
            "city": "Test City",
            "card": "4111111111111111",
            "month": "12",
            "year": "2025"
        }
        
        self.order_page.fill_order_form(**test_data)
        self.order_page.click_purchase()
        
        assert "Thank you for your purchase" in self.order_page.get_order_confirmation_text()
        
        order_details = self.order_page.get_order_details()
        assert order_details["Id"] != ""
        assert order_details["Amount"] != ""
        assert order_details["Card Number"] == test_data["card"]
        
        self.logger.info("Successful order confirmation test passed")

    def test_unsuccessful_order(self):
        self.logger.info("===== TESTING UNSUCCESSFUL ORDER =====")
        test_data = {
            "name": "",
            "country": "Test Country",
            "city": "Test City",
            "card": "",
            "month": "12",
            "year": "2025"
        }
        
        self.order_page.fill_order_form(**test_data)
        self.order_page.click_purchase()
        
        alert_text = self.order_page.get_alert_text()
        
        assert "Please fill out Name and Creditcard" in alert_text
        
        
        self.logger.info("UnSuccessful order test passed")