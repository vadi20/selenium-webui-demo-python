from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.config import Config

class DriverManager:
    @staticmethod
    def get_driver():
        if Config.BROWSER.lower() == "chrome":
            options = webdriver.ChromeOptions()
            if Config.HEADLESS:
                options.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        elif Config.BROWSER.lower() == "firefox":
            driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        else:
            raise ValueError(f"Unsupported browser: {Config.BROWSER}")
        
        driver.maximize_window()
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        return driver