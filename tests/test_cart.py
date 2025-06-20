import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.logger import get_logger
from utils.json_reader import JSONReader
import re


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


@pytest.mark.wip
class TestCartAdvanced:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.logger = get_logger(f"test.{self.__class__.__name__}")

        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)

        self.test_data = JSONReader.get_data("cart_data.json", "test_cases")

        
        self.home_page.navigate_to_home()
        self.home_page.click_cart_menu()
        self.cart_page.delete_all_items()

    @pytest.mark.parametrize("test_case", JSONReader.get_data("cart_data.json", "test_cases"))
    def test_multiple_products_cart(self, test_case):
        self.logger.info(f"Testing cart with {len(test_case['products'])} products")
        
        expected_items = []

        regex = r"\$(\s*[.,\d]+)"
        
        for product in test_case["products"]:
            self.home_page.navigate_to_home()
            self.home_page.select_category(product["category"])
            
            found = self.home_page.find_and_select_product(product["name"])
            assert found, f"Product {product['name']} not found"
            
            alert_text = self.product_page.add_to_cart()
            assert "Product added" in alert_text, "Add to cart failed"
            
            expected_items.append({
                "name": product["name"],
                "price": float((re.search(regex,self.product_page.get_product_price())).group(1))
            })
        
        self.home_page.click_cart_menu()
        self.cart_page.validate_cart_contents(expected_items)
        
        self.logger.info(f"Successfully validated cart with {len(expected_items)} products")