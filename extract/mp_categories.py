import os
from time import sleep

from django.core.wsgi import get_wsgi_application
from services.selenium_service import SeleniumService, SeleniumDebuggerDriver
from selenium.webdriver.common.by import By

from utils.date_format import parse_day_month, parse_month_year
from utils.string_format import parse_amount_to_float

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data.settings")
application = get_wsgi_application()
from data.models import Records, Categories

WEB = "https://www.mercadopago.com.ar/finance/spending-tracking"


def get_action(driver):
    xp_description = ".//p[@class='ui-rowfeed-description__text']"
    description = driver.find_element(By.XPATH, value=xp_description).text
    return description

def get_title(driver):
    xp_title = ".//span[@class='ui-rowfeed-title']"
    title = driver.find_element(By.XPATH, value=xp_title).text
    return title

def get_amount(driver):
    xp_amount = ".//span[@class='andes-money-amount ui-rowfeed-amount ui-rowfeed-amount--primary-color andes-money-amount--cents-comma']"
    amount = driver.find_element(By.XPATH, value=xp_amount)
    return parse_amount_to_float(amount.accessible_name)

def get_date(driver, date):
    xp_day_month = ".//p[@class='ui-rowfeed-date']"
    str_date = driver.find_element(By.XPATH, value=xp_day_month).text
    cur_date = parse_day_month(str_date, date.year)
    return cur_date

def get_id(driver):
    xp_id = ".//span[@class='c-copy-operation__text c-copy-operation__text--initial']"
    id = driver.find_element(By.XPATH, value=xp_id).text
    return id.strip().split()[-1]

def save(*args, **kwargs):
    id = kwargs["id"]
    description = kwargs["description"]
    amount = kwargs["amount"]
    category = kwargs["category"]
    date = kwargs["date"]
    record = Records(id=id, description=description, amount=float(amount), category=category, date=date)
    record.save()

def perform_save(id, description, amount, category, date):
    category_obj = Categories.objects.filter(name__icontains=category).first()
    save(id=id, description=description, amount=amount, category=category_obj, date=date)


def category_detail(category, driver, date):
    xp_cat_name = ".//span[contains(@class, 'andes-list__item-primary')]"
    xp_cat_list = ".//div[@class='detail-row-wrapper']"

    category_name = category.find_element(By.XPATH, value=xp_cat_name).text
    category.click()
    cat_list = driver.find_elements(By.XPATH, value=xp_cat_list)
    for item in range(len(cat_list)):
        action = get_action(cat_list[item])
        title = get_title(cat_list[item])
        amount = get_amount(cat_list[item])
        item_date = get_date(cat_list[item], date)
        cat_list[item].click()
        operation_id = get_id(driver)
        print(operation_id, action, title, amount, item_date)
        driver.driver.back()  # execute_script("window.history.go(-1)")
        cat_list = driver.find_elements(By.XPATH, value=xp_cat_list)
        perform_save(operation_id, f"{title} - {action}", amount, category_name, item_date)




def main_category():
    driver = SeleniumService(SeleniumDebuggerDriver().driver)
    driver.get(WEB)

    xp_categories = "//ul[@aria-label='Listado de categorías organizadas del mayor al menor gasto.']//li"
    xp_label_date = "//div[@class='navigator__date']"

    container_categories = driver.find_elements(By.XPATH, value=xp_categories)
    categories_count = len(container_categories)
    label_date = driver.find_element(By.XPATH, value=xp_label_date).text
    current_date = parse_month_year(label_date)

    for i in range(categories_count):
        driver.get(WEB)
        categories = driver.find_elements(By.XPATH, value=xp_categories)
        category = categories[i]
        sleep(1)
        category_detail(category, driver, current_date)


if __name__ == '__main__':
    main_category()
