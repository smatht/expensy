"""Selenium service for web automation and browser control."""

from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


# Chrome debugging setup instructions:
# chrome --remote-debugging-port=9222 --user-data-dir=remote-profile
# "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
# --remote-debugging-port=9222 --user-data-dir="C:\remote-profile"
DRIVER_PATH = "C:\\chromedriver.exe"


class SeleniumService:
    """
    Selenium service wrapper for common web automation operations.

    This class provides a simplified interface for common Selenium operations
    like finding elements, clicking, and sending keys.
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize the Selenium service with a WebDriver instance.

        Args:
            driver: WebDriver instance to use for automation
        """
        self.driver = driver

    def get(self, url: str) -> None:
        """
        Navigate to a specific URL.

        Args:
            url: The URL to navigate to
        """
        self.driver.get(url)

    def find_element(self, by: By, value: str) -> WebElement:
        """
        Find a single element on the page.

        Args:
            by: The method to use for finding the element (e.g., By.ID,
                By.CLASS_NAME)
            value: The value to search for

        Returns:
            WebElement if found

        Raises:
            NoSuchElementException: If the element is not found
        """
        return self.driver.find_element(by, value)

    def find_elements(self, by: By, value: str) -> List[WebElement]:
        """
        Find multiple elements on the page.

        Args:
            by: The method to use for finding elements (e.g., By.TAG_NAME)
            value: The value to search for

        Returns:
            List of WebElements (empty list if none found)
        """
        return self.driver.find_elements(by, value)

    def click(self, element: WebElement) -> None:
        """
        Click on a web element.

        Args:
            element: The WebElement to click on
        """
        element.click()

    def send_keys(self, element: WebElement, value: str) -> None:
        """
        Send text to a web element.

        Args:
            element: The WebElement to send text to
            value: The text to send
        """
        element.send_keys(value)

    def wait(self, seconds: int) -> None:
        """
        Set implicit wait time for the driver.

        Args:
            seconds: Number of seconds to wait
        """
        self.driver.implicitly_wait(seconds)

    def close(self) -> None:
        """
        Close the browser and quit the driver.
        """
        self.driver.quit()


class SeleniumDebuggerDriver:
    """
    Chrome driver configured for debugging mode.

    This driver connects to an existing Chrome instance running in debug mode,
    allowing for inspection and debugging of automation scripts.
    """

    def __init__(self):
        """
        Initialize the debugger driver with Chrome options.
        """
        options = Options()
        options.add_experimental_option("debuggerAddress", "localhost:9222")
        # options.add_argument("--start-maximized")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # service = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(options=options)
        self.driver = driver


class SeleniumDriver:
    """
    Standard Chrome driver for web automation.

    This driver creates a new Chrome instance with standard automation settings.
    """

    def __init__(self):
        """
        Initialize the standard driver with Chrome options.
        """
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        service = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(
            service=service, options=options
        )
        self.driver=driver
