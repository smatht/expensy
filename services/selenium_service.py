from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver



DRIVER_PATH = "C:\chrome-win64\chrome.exe"



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
        # service = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(options=options)
        self.driver = driver

class SeleniumDriver:

    def __init__(self):
        service = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome()
        self.driver = driver