import pytest
from pages.home_page import HomePage
from utils.logger import get_logger


@pytest.mark.usefixtures("setup")
class TestHomePage:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.logger = get_logger(f"test.{self.__class__.__name__}")

    def test_home_page_title(self):
        self.logger.info("===== TESTING HOME PAGE TITLE =====")
        home_page = HomePage(self.driver,self.config)
        home_page.navigate_to_home()
        assert "STORE" in self.driver.title
        self.logger.info("Home page title test passed")
    
    def test_navigation_menu_items(self):
        self.logger.info("===== TESTING NAVIGATION MENU ITEMS =====")
        home_page = HomePage(self.driver,self.config)
        home_page.navigate_to_home()
        
        assert home_page.is_visible(home_page.HOME_MENU)
        assert home_page.is_visible(home_page.CONTACT_MENU)
        assert home_page.is_visible(home_page.ABOUT_US_MENU)
        assert home_page.is_visible(home_page.CART_MENU)
        assert home_page.is_visible(home_page.LOGIN_MENU)
        assert home_page.is_visible(home_page.SIGNUP_MENU)
        
        self.logger.info("Navigation menu items test passed")
    
    def test_carousel_functionality(self):
        self.logger.info("===== TESTING CAROUSEL FUNCTIONALITY =====")
        home_page = HomePage(self.driver,self.config)
        home_page.navigate_to_home()
        
        initial_index = home_page.get_active_carousel_item_index()
        home_page.navigate_carousel("next")
        next_index = home_page.get_active_carousel_item_index()
        assert next_index != initial_index
        
        home_page.navigate_carousel("prev")
        prev_index = home_page.get_active_carousel_item_index()
        assert prev_index == initial_index
        
        self.logger.info("Carousel functionality test passed")
    
    def test_categories_section(self):
        self.logger.info("===== TESTING CATEGORIES SECTION =====")
        home_page = HomePage(self.driver,self.config)
        home_page.navigate_to_home()
        
        assert "CATEGORIES" in home_page.get_categories_title()
        
        home_page.select_category("Phones")
        assert home_page.get_product_count() > 0
        
        home_page.select_category("Laptops")
        assert home_page.get_product_count() > 0
        
        home_page.select_category("Monitors")
        assert home_page.get_product_count() > 0
        
        self.logger.info("Categories section test passed")