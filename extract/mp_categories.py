"""Mercado Pago transaction extraction module."""

import os
from time import sleep


from django.core.wsgi import get_wsgi_application
from services.selenium_service import SeleniumService, SeleniumDebuggerDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils.date_format import parse_day_month, parse_month_year
from utils.string_format import parse_amount_to_float

# Django configuration
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data.settings")
application = get_wsgi_application()

from data.models import Records, Categories

# Configuration constants
WEB_URL = "https://www.mercadopago.com.ar/finance/spending-tracking"
SOURCE = "mercado pago"


def get_action(driver: WebElement) -> str:
    """
    Extract the action/description from a transaction element.

    Args:
        driver: WebElement containing the transaction data

    Returns:
        Transaction description text
    """
    xp_description = ".//p[@class='ui-rowfeed-description__text']"
    description = driver.find_element(By.XPATH, value=xp_description).text
    return description


def get_title(driver: WebElement) -> str:
    """
    Extract the title from a transaction element.

    Args:
        driver: WebElement containing the transaction data

    Returns:
        Transaction title text
    """
    xp_title = ".//span[@class='ui-rowfeed-title']"
    title = driver.find_element(By.XPATH, value=xp_title).text
    return title


def get_amount(driver: WebElement) -> float:
    """
    Extract and parse the amount from a transaction element.

    Args:
        driver: WebElement containing the transaction data

    Returns:
        Parsed amount as float
    """
    xp_amount = (
        ".//span[@class='andes-money-amount ui-rowfeed-amount "
        "ui-rowfeed-amount--primary-color andes-money-amount--cents-comma']"
    )
    amount = driver.find_element(By.XPATH, value=xp_amount)
    return parse_amount_to_float(amount.accessible_name)


def get_date(driver: WebElement, date) -> str:
    """
    Extract and parse the date from a transaction element.

    Args:
        driver: WebElement containing the transaction data
        date: Reference date object for year/month context

    Returns:
        Parsed date string
    """
    xp_day_month = ".//p[@class='ui-rowfeed-date']"
    str_date = driver.find_element(By.XPATH, value=xp_day_month).text
    cur_date = parse_day_month(str_date, date.year, date.month)
    return cur_date


def get_id(driver: WebElement) -> str:
    """
    Extract the operation ID from a transaction element.

    Args:
        driver: WebElement containing the transaction data

    Returns:
        Operation ID string
    """
    xp_id = (
        ".//span[@class='c-copy-operation__text "
        "c-copy-operation__text--initial']"
    )
    operation_id = driver.find_element(By.XPATH, value=xp_id).text
    return operation_id.strip().split()[-1]


def save_record(**kwargs) -> None:
    """
    Save a transaction record to the database.

    Args:
        **kwargs: Record data including id, description, amount, category, date
    """
    record_id = kwargs["id"]
    description = kwargs["description"]
    amount = kwargs["amount"]
    category = kwargs["category"]
    date = kwargs["date"]

    try:
        Records.objects.get(pk=record_id)
    except Records.DoesNotExist:
        record = Records(
            id=record_id,
            description=description,
            amount=float(amount),
            category=category,
            date=date,
            source=SOURCE
        )
        record.save()


def perform_save(
    record_id: str,
    description: str,
    amount: float,
    category: str,
    date
) -> None:
    """
    Perform the save operation with category lookup.

    Args:
        record_id: Unique identifier for the record
        description: Transaction description
        amount: Transaction amount
        category: Category name to search for
        date: Transaction date
    """
    category_obj = Categories.objects.filter(name__icontains=category).first()
    save_record(
        id=record_id,
        description=description,
        amount=amount,
        category=category_obj,
        date=date
    )


def category_detail(category: WebElement, driver, date) -> None:
    """
    Process transactions within a specific category.

    Args:
        category: WebElement representing the category
        driver: Selenium driver instance
        date: Reference date for transaction processing
    """
    xp_cat_name = ".//span[contains(@class, 'andes-list__item-primary')]"
    xp_cat_list = ".//div[@class='detail-row-wrapper']"

    # Get category name and click to expand
    category_name = category.find_element(By.XPATH, value=xp_cat_name).text
    category.click()

    # Get list of transactions in this category
    cat_list = driver.find_elements(By.XPATH, value=xp_cat_list)

    # Process each transaction
    for item in range(len(cat_list)):
        action = get_action(cat_list[item])
        title = get_title(cat_list[item])
        amount = get_amount(cat_list[item])
        item_date = get_date(cat_list[item], date)

        # Click to get operation details
        cat_list[item].click()
        sleep(1)
        operation_id = get_id(driver)

        print(operation_id, action, title, amount, item_date)

        # Navigate back and refresh list
        driver.driver.back()
        sleep(1)
        cat_list = driver.find_elements(By.XPATH, value=xp_cat_list)

        # Save the transaction
        perform_save(
            operation_id,
            f"{title} - {action}",
            amount,
            category_name,
            item_date
        )


def main_category() -> None:
    """
    Main function to extract Mercado Pago transactions by category.

    This function:
    1. Connects to Mercado Pago spending tracking page
    2. Gets the list of spending categories
    3. Processes each category to extract transactions
    4. Saves new transactions to the database
    """
    # Initialize Selenium driver
    driver = SeleniumService(SeleniumDebuggerDriver().driver)
    driver.get(WEB_URL)

    # Define XPath selectors
    xp_categories = (
        "//ul[@aria-label='Listado de categorías organizadas del mayor al "
        "menor gasto.']//li"
    )
    xp_label_date = "//div[@class='navigator__date']"

    # Get categories and date information
    container_categories = driver.find_elements(By.XPATH, value=xp_categories)
    categories_count = len(container_categories)
    label_date = driver.find_element(By.XPATH, value=xp_label_date).text
    current_date = parse_month_year(label_date)

    # Process each category
    for i in range(categories_count):
        driver.get(WEB_URL)
        categories = driver.find_elements(By.XPATH, value=xp_categories)
        category = categories[i]
        sleep(1)
        category_detail(category, driver, current_date)


if __name__ == '__main__':
   main_category()
