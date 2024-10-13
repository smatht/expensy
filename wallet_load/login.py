import os
from time import sleep

from services.selenium_service import SeleniumService

WEB = "https://web.budgetbakers.com/login"
EMAIL = os.getenv("WALLET_EMAIL")
PASS = os.getenv("WALLET_PASS")


def login(driver: SeleniumService):
    driver.get(WEB)

    sleep(5)
    email = driver.find_element(by="xpath", value='//input[@name="email"]')
    password = driver.find_element(by="xpath", value='//input[@name="password"]')
    logging_button = driver.find_element(by='xpath', value='//button[text()="Log In"]' )

    email.send_keys(EMAIL)
    password.send_keys(PASS)
    logging_button.click()

