from time import sleep

from services.selenium_service import SeleniumService, SeleniumDebuggerDriver
from selenium.webdriver.common.by import By


WEB = "https://www.mercadopago.com.ar/finance/spending-tracking"


def get_operation_number(driver, expense_obj):
    OP_NUM = "Número de operación"
    sleep(1)
    expense_obj.click()

    op_label = driver.find_element(by="xpath", value=f"//span[contains(text(), '{OP_NUM}')]").text
    op_number = op_label.replace(OP_NUM, "").replace(" ", "")

    return op_number

def get_amount(section):
    spans = section.find_elements(by='xpath', value='./span')
    amount_split = []
    for span in spans:
        amount_split.append(span.text)
    try:
        amount = float(amount_split[2].replace(".", ""))
    except ValueError:
        amount = float(amount_split[1].replace(".", ""))
    return amount



def extract_from_category(driver, category_name, category_obj):
    sleep(1)
    category_obj.click()

    container_expenses = driver.find_elements(by="xpath",
                                             value="//ul[@class='andes-list__group--sublist' and @aria-labelledby='basic-list-0']/div")
    for expense_list in container_expenses:
        description_amount = expense_list.find_elements(by="xpath", value="./li/a/section/div[@class='ui-rowfeed-content-rows']/div/span")
        description = description_amount[0].text
        amount = get_amount(description_amount[1])
        expense_detail = get_operation_number(driver, expense_list)
        print(category_name, description, amount, expense_detail)


def extract():
    driver = SeleniumService(SeleniumDebuggerDriver().driver)
    driver.get(WEB)

    # button_previous_month = driver.find_element(by="xpath", value="//button[@data-testid='month-button-previous']")
    # button_previous_month.click()

    xp_categories = "//ul[@aria-label='Listado de categorías organizadas del mayor al menor gasto.']//li"
    xp_cat_name = ".//span[contains(@class, 'andes-list__item-primary')]"

    container_categories = driver.find_elements(By.XPATH, value=xp_categories)
    for i in range(len(container_categories)):
        category_name = container_categories[i].find_element(By.XPATH, value=xp_cat_name).text
        extract_from_category(driver, category_name, container_categories[i])

        driver.get(WEB)
        container_categories = driver.find_elements(By.XPATH, value=xp_categories)

    driver.get(WEB)
    button_previous_month = driver.find_element(by="xpath", value="//button[@data-testid='month-button-previous']")
    button_previous_month.click()

    container_categories = driver.find_elements(By.XPATH, value=xp_categories)
    for i in range(len(container_categories)):
        category_name = container_categories[i].find_element(By.XPATH, value=xp_cat_name).text
        extract_from_category(driver, category_name, container_categories[i])

        driver.get(WEB)
        button_previous_month = driver.find_element(by="xpath", value="//button[@data-testid='month-button-previous']")
        button_previous_month.click()

        container_categories = driver.find_elements(By.XPATH, value=xp_categories)


def extract_category():
    driver = SeleniumService(SeleniumDebuggerDriver().driver)
    driver.get(WEB)

    xp_categories = "//ul[@aria-label='Listado de categorías organizadas del mayor al menor gasto.']//li"
    xp_cat_name = ".//span[contains(@class, 'andes-list__item-primary')]"

    container_categories = driver.find_elements(By.XPATH, value=xp_categories)
    for category in container_categories:
        category_name = category.find_element(By.XPATH, value=xp_cat_name).text
        category_amount =


if __name__ == '__main__':
    extract_category()