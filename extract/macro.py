import hashlib
import os
from time import sleep

from utils.category_inference import macro_inference
from services.selenium_service import SeleniumService, SeleniumDebuggerDriver
from django.core.wsgi import get_wsgi_application

from utils.date_format import parse_day_month_year

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data.settings")
application = get_wsgi_application()
from data.models import Records, Categories

path = "/Users/msticchi/Documents/dev/matias/scraping/chrome-driver"
web = "https://www.macro.com.ar/bancainternet/#"
SRC = "macro"

def get_record_id(text: str) -> str:
    return hashlib.sha1(text.encode('ascii')).hexdigest()


def extract():
    driver = SeleniumService(SeleniumDebuggerDriver().driver)
    driver.get(web)
    # menu_detalle = WebDriverWait(driver.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@onclick='executeMenuOption(\'menuCuentas_86291583\',\'itemSelection\',\'menuTableWidget86291583\', \'Movs\');'")))
    menu_movs = driver.find_elements(by="xpath", value="//li[@id='menu_movs']")
    driver.driver.execute_script("arguments[0].click();", menu_movs[1])
    # WebDriverWait(driver.driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='richText1']/p")))
    sleep(10)
    movs = driver.find_elements(by="xpath", value="//tr[@class='evenRow' or @class='oddRow']")

    for mov in movs:
        description = mov.find_element(by="xpath", value="./td[@headers='_Descripción']").text
        category_id = macro_inference(description)
        if category_id == 0:
            continue
        date = mov.find_element(by="xpath", value="./td[@headers='_Fecha']").text
        date_obj = parse_day_month_year(date)
        transaction_number = mov.find_element(by="xpath", value="./td[@headers='_Nro. transacción']").text
        amount = mov.find_element(by="xpath", value="./td[@headers='_Importe']").text
        amount = amount.replace("$ ", "").replace(".", "").replace(",", ".")

        record_id = get_record_id(f"{date},{transaction_number},{amount}")
        category = Categories.objects.get(pk=category_id)
        record = Records(id=record_id, description=f"{description}. {date}", amount=float(amount), category=category,
                         date=date_obj, source=SRC)
        record.save()


if __name__ == '__main__':
    extract()
