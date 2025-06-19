import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from utils.logger import get_logger
from utils.excel_reader import ExcelReader


@pytest.mark.usefixtures("setup")
class TestProducts:
    @pytest.fixture(params=ExcelReader.get_data("testdata.xlsx", "Products"))
    def product_data(self, request):
        return request.param

    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.logger = get_logger(f"test.{self.__class__.__name__}")
        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        
        self.home_page.navigate_to_home()

    def test_product_listing_by_category(self):
        self.logger.info("===== TESTING PRODUCT LISTING BY CATEGORY =====")
        
        self.home_page.select_category("Phones")
        
        self.home_page.select_default_product()
        
        product_details = self.product_page.get_product_details()
        assert product_details["name"] != ""
        assert '$' in product_details["price"]
        assert product_details["description"] != ""
        #assert product_details["image_loaded"] is True
        
        self.logger.info("Product listing by category test passed")
    
    def test_add_product_to_cart(self):
        self.logger.info("===== TESTING ADD PRODUCT TO CART =====")

        self.home_page.select_category("Laptops")
        
        self.home_page.select_default_product()
        
        product_name = self.product_page.get_product_name()
        alert_text = self.product_page.add_to_cart()
        
        assert "Product added" in alert_text
        

        self.home_page.click_cart_menu()

        self.logger.info("Add product to cart test passed")
    
    '''@pytest.mark.parametrize("category", ["Phones", "Laptops", "Monitors"])
    def test_product_categories(self, category):
        self.logger.info(f"===== TESTING PRODUCT CATEGORY: {category} =====")
        
        self.home_page.select_category(category)
        
        product_count = self.home_page.get_product_count()
        assert product_count > 0
        
        self.logger.info(f"Product category {category} test passed")'''

    def test_product_categories(self, product_data):
        self.logger.info(f"===== Testing: {product_data['test_name']} =====")
        
        self.home_page.select_category(product_data["category"])
        
        product_count = self.home_page.get_product_count()
        assert product_count == product_data["expected_product_count"]
        
        self.logger.info(f"Test '{product_data['test_name']}' passed")

    def test_select_specific_product(self):
        self.logger.info("===== Testing product navigation =====")
        
        self.home_page.navigate_to_home()
        
        product_found = self.home_page.find_and_select_product("Apple monitor 24")
        
        assert product_found, "Product not found"
        
        product_name = self.product_page.get_product_name()
        assert "Apple monitor 24" in product_name
        self.logger.info(f"Successfully navigated to product: {product_name}")