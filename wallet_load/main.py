from time import sleep

from exceptiongroup import catch
from selenium.common import NoSuchElementException

from services.selenium_service import SeleniumService, SeleniumDebuggerDriver
from wallet_load.login import login

if __name__ == '__main__':
    driver = SeleniumService(SeleniumDebuggerDriver().driver)
    login(driver)
    sleep(20)

    # while True:
    #     try:
    #         driver.find_element(by="xpath", value="//nav/ul/li/a[text()=Dashboard]")
    #         print('olg2')
    #     except NoSuchElementException:
    #         print('olga')
    #         sleep(2)

    driver.get("https://web.budgetbakers.com/records")
    sleep(5)
    add_button = driver.find_element(by="xpath", value="//div[@class='_1DUmJhdlzGa5I26eA2LOma']/button")
    add_button.click()

    expense_button = driver.find_element(by="xpath", value="//div[@class='field icon-select']")
    expense_button.click()
    sleep(2)
    select_otros_gastos = driver.find_element(by="xpath", value="//div[@class='icon-option text']/div[text()='Otros gastos']")
    select_otros_gastos.click()

    amount_field = driver.find_element(by="xpath", value="//div[@class='ui input']/input[@name='amount']")
    amount_field.send_keys(999)

    # Busca el select de categoria y busca una categoria por nombre usando el buscador
    category_field = driver.find_element(by="xpath",
                            value="//div[@class='field']/div/div[contains(@class, 'field select-category')]")
    category_field.click()
    sleep(2)
    category_search = driver.find_element(by="xpath",
                            value="//div[contains(@class, 'field select-category')]/div/div/div/div/input[@placeholder='Search']")
    category_field.click()
    category_search.send_keys('home')
    category_options = driver.find_elements(by="xpath",
                             value="//div[@class='field']/div/div[contains(@class, 'field select-category')]/div/div[contains(@class, 'menu transition visible')]/*/ul/li")
    category_options[0].click()

    description = driver.find_element(by="xpath", value="//div[contains(@class, 'field field-note')]/textarea")
    description.send_keys("Esto es una prueba")

    submit_button = driver.find_element(by="xpath", value="//button[text()='Add record']")
    submit_button.click()

    # load_data('data/path/file.csv')