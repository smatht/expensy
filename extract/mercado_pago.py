from time import sleep

from services.selenium_service import SeleniumService, SeleniumDebuggerDriver


WEB = "https://www.mercadopago.com.ar/finance/spending-tracking"


def get_expense_detail(driver, expense_obj):
    OP_NUM = "Número de operación"
    sleep(1)
    expense_obj.click()

    op_label = driver.find_element(by="xpath", value=f"//span[contains(text(), '{OP_NUM}')]").text
    op_number = op_label.replace(OP_NUM, "").replace(" ", "")

    op_type = driver.find_element(by="xpath", value="")

    return {
        "operation_number": op_number
    }

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
        amount_section = expense_list.find_element(by="xpath", value="./li/a/section/div[@class='ui-rowfeed-content-rows']/div/span")
        amount = get_amount(amount_section)
        expense_detail = get_expense_detail(driver, expense_list)


def extract():
    driver = SeleniumService(SeleniumDebuggerDriver().driver)
    driver.get(WEB)

    container_categories = driver.find_elements(by="xpath", value="//ul[@id=':R5b9m:']/div[@class='categories__item-wrapper']")
    for categories in container_categories:
        category_name = categories.find_element(by="xpath", value="./li/div/div[@class='andes-list__item-text']/span").text
        extract_from_category(driver, category_name, categories)
        break

if __name__ == '__main__':
    extract()