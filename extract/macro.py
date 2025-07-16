"""Macro bank transaction extraction module."""

import hashlib
import os
from time import sleep

from utils.category_inference import macro_inference
from services.selenium_service import SeleniumService, SeleniumDebuggerDriver
from django.core.wsgi import get_wsgi_application
from utils.date_format import parse_day_month_year

# Django configuration
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data.settings")
application = get_wsgi_application()

from data.models import Records, Categories

# Configuration constants
PATH = "/Users/msticchi/Documents/dev/matias/scraping/chrome-driver"
WEB_URL = "https://www.macro.com.ar/bancainternet/#"
SOURCE = "macro"


def get_record_id(text: str) -> str:
    """
    Generate a unique record ID using SHA1 hash.

    Args:
        text: Text to hash (combination of date, transaction number, and amount)

    Returns:
        SHA1 hash string of the input text

    Examples:
        >>> get_record_id("2024-01-15,12345,100.50")
        'a1b2c3d4e5f6...'
    """
    return hashlib.sha1(text.encode('ascii')).hexdigest()


def extract_macro_transactions() -> None:
    """
    Extract and save Macro bank transactions.

    This function:
    1. Connects to Macro bank website using Selenium
    2. Navigates to the movements section
    3. Extracts transaction data from the table
    4. Processes and saves new transactions to the database
    5. Skips transactions that don't match any category
    """
    # Initialize Selenium driver
    driver = SeleniumService(SeleniumDebuggerDriver().driver)
    driver.get(WEB_URL)

    # Navigate to movements section
    menu_movs = driver.find_elements(by="xpath", value=".//li[@id='menu_movs']")
    driver.driver.execute_script("arguments[0].click();", menu_movs[1])

    # Wait for page to load
    sleep(10)

    # Find all transaction rows
    movs = driver.find_elements(
        by="xpath",
        value="//tr[@class='evenRow' or @class='oddRow']"
    )

    # Process each transaction
    for mov in movs:
        # Extract transaction details
        description = mov.find_element(
            by="xpath",
            value="./td[@headers='_Descripción']"
        ).text

        # Infer category based on description
        category_id = macro_inference(description)
        if category_id == 0:
            continue

        # Extract date and convert to date object
        date = mov.find_element(
            by="xpath",
            value="./td[@headers='_Fecha']"
        ).text
        date_obj = parse_day_month_year(date)

        # Extract transaction number
        transaction_number = mov.find_element(
            by="xpath",
            value="./td[@headers='_Nro. transacción']"
        ).text

        # Extract and clean amount
        amount = mov.find_element(
            by="xpath",
            value="./td[@headers='_Importe']"
        ).text
        amount = amount.replace("$ ", "").replace(".", "").replace(",", ".")

        # Generate unique record ID
        record_id = get_record_id(f"{date},{transaction_number},{amount}")

        # Get category object
        category = Categories.objects.get(pk=category_id)

        # Save record if it doesn't exist
        try:
            Records.objects.get(pk=record_id)
        except Records.DoesNotExist:
            record = Records(
                id=record_id,
                description=f"{description}. {date}",
                amount=float(amount),
                category=category,
                date=date_obj,
                source=SOURCE
            )
            record.save()


if __name__ == '__main__':
    extract_macro_transactions()
