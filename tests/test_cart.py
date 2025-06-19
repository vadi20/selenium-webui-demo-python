import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.logger import get_logger


@pytest.mark.usefixtures("setup")
class TestCart:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.logger = get_logger(f"test.{self.__class__.__name__}")

        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        
        self.home_page.navigate_to_home()
        self.home_page.select_category("Phones")
        self.home_page.select_default_product()
        self.alert_text = self.product_page.add_to_cart()
        
    
    def test_add_single_item_to_cart(self):
        self.logger.info("===== TESTING ADD SINGLE ITEM TO CART =====")
        assert "Product added" in self.alert_text

        self.home_page.click_cart_menu()
        
        assert self.cart_page.get_cart_items_count() == 1
        self.logger.info("Add single item to cart test passed")
    
    def test_remove_item_from_cart(self):
        self.logger.info("===== TESTING REMOVE ITEM FROM CART =====")
        self.home_page.click_cart_menu()
        
        initial_count = self.cart_page.get_cart_items_count()
        self.cart_page.delete_item(0)
        
        self.home_page.wait.until(lambda d: self.cart_page.get_cart_items_count() < initial_count)
        
        assert self.cart_page.get_cart_items_count() == 0
        self.logger.info("Remove item from cart test passed")
    
    def test_place_order_flow(self):
        self.logger.info("===== TESTING PLACE ORDER FLOW =====")
        self.home_page.click_cart_menu()
        self.cart_page.click_place_order()
        
        assert self.cart_page.is_visible(self.cart_page.ITEM_NAMES)
        assert self.cart_page.is_visible(self.cart_page.PLACE_ORDER_BUTTON)
        
        self.logger.info("Place order flow test passed")


class TestCartAdvanced:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.logger = get_logger(f"test.{self.__class__.__name__}")

        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        
        self.home_page.navigate_to_home()