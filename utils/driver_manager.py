from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class DriverManager:
    @staticmethod
    def get_driver():
        from configparser import ConfigParser
        config = ConfigParser()
        config.read('config/config.ini')
        browser = config.get('DEFAULT', 'browser', fallback='chrome').lower()
        headless = config.getboolean('DEFAULT', 'headless', fallback=False)
        implicit_wait = config.get('DEFAULT', 'implicit_wait')

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        elif browser == "firefox":
            driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        driver.maximize_window()
        driver.implicitly_wait(implicit_wait)
        return driver
    

