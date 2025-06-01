from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


# how_to_open_debugging_chrome:
# chrome --remote-debugging-port=9222 --user-data-dir=remote-profile
# "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\remote-profile"
DRIVER_PATH = "C:\chromedriver.exe"



class SeleniumService:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get(self, url: str) -> None:
        self.driver.get(url)

    def find_element(self, by: By, value: str) -> WebElement:
        return self.driver.find_element(by, value)

    def find_elements(self, by: By, value: str) -> List[WebElement]:
        return self.driver.find_elements(by, value)

    def click(self, element: WebElement) -> None:
        element.click()

    def send_keys(self, element: WebElement, value: str) -> None:
        element.send_keys(value)

    def wait(self, seconds: int) -> None:
        self.driver.implicitly_wait(seconds)

    def close(self) -> None:
        self.driver.quit()


class SeleniumDebuggerDriver:

    def __init__(self):
        options = Options()
        options.add_experimental_option("debuggerAddress", "localhost:9222")
        # options.add_argument("--start-maximized")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # service = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(options=options)
        self.driver = driver

class SeleniumDriver:

    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        service = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        self.driver = driver