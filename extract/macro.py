from time import sleep

import pandas as pd

from services.selenium_service import SeleniumService, SeleniumDebuggerDriver

# how_to_open_debugging_chrome = "chrome --remote-debugging-port=9222 --user-data-dir=remote-profile"
path = "/Users/msticchi/Documents/dev/matias/scraping/chrome-driver"
web = "https://www.macro.com.ar/bancainternet/#"


def extract():
    driver = SeleniumService(SeleniumDebuggerDriver().driver)
    driver.get(web)
    # menu_detalle = WebDriverWait(driver.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@onclick='executeMenuOption(\'menuCuentas_86291583\',\'itemSelection\',\'menuTableWidget86291583\', \'Movs\');'")))
    menu_movs = driver.find_elements(by="xpath", value="//li[@id='menu_movs']")
    driver.driver.execute_script("arguments[0].click();", menu_movs[1])
    # WebDriverWait(driver.driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='richText1']/p")))
    sleep(10)
    movs = driver.find_elements(by="xpath", value="//tr[@class='evenRow' or @class='oddRow']")

    dic = []
    for mov in movs:
        date = mov.find_element(by="xpath", value="./td[@headers='_Fecha']").text
        transaction_number = mov.find_element(by="xpath", value="./td[@headers='_Nro. transacción']").text
        description = mov.find_element(by="xpath", value="./td[@headers='_Descripción']").text
        amount = mov.find_element(by="xpath", value="./td[@headers='_Importe']").text
        dic.append({
            "date": date,
            "transaction_number": transaction_number,
            "description": description,
            "amount": amount
        })
    data = pd.DataFrame(dic)
    data.to_csv("test.csv")

if __name__ == '__main__':
    extract()