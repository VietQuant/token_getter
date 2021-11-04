import threading
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
import settings
import os
logging.basicConfig(format='%(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--proxy-server=192.168.1.122:1412')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options



if __name__ == '__main__':
    from rework_backtrader.utils.file_accessor import FileAccessor
    from datetime import datetime, timedelta
    from urllib.parse  import parse_qsl

    remote = os.getenv("REMOTE_CHROME", None)
    if remote:
        chrome_options = set_chrome_options()
        capabilities = {
                "browserName": "chrome",
            }
        capabilities.update(chrome_options.to_capabilities())
        driver = webdriver.Remote(command_executor=remote, 
                                    desired_capabilities=capabilities, \
                                    seleniumwire_options={
                                        'auto_config': False,
                                        'addr': '0.0.0.0',
                                        'port': 1412
                                        })
    else:
        driver = webdriver.Chrome(executable_path="drivers/chromedriver", options=set_chrome_options())

    driver.get("https://finance.vietstock.vn")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'btn-request-call-login')))
    driver.find_element_by_id("btn-request-call-login").click()
    driver.find_element_by_id('txtEmailLogin').send_keys('doantvinh@gmail.com')
    driver.find_element_by_id('txtPassword').send_keys('Vietquant001')
    driver.find_element_by_id('btnLoginAccount').click()

    driver.get("https://finance.vietstock.vn/lich-su-kien.htm?page=1")
    cookies = driver.get_cookies()
    FileAccessor.write_json("vietstock_cookies.json", cookies)
    today = datetime.now()
    from_time = today - timedelta(days=7)
    to_time = today + timedelta(days=7)
    driver.get("https://finance.vietstock.vn/lich-su-kien.htm?page=1&from={}&to={}&tab=1&group=13&exchange=-1".format(from_time.date(), to_time.date()))
    for request in driver.requests:
        if request.response:
            if "eventstypedata" in request.url:
                print(request.url)
                body = dict(parse_qsl(request._body.decode('UTF-8')))
                FileAccessor.write_json("vietstock_bodies.json", body)
    driver.get("https://finance.vietstock.vn/ket-qua-giao-dich")
    for request in driver.requests:
        if request.response:
            if "KQGDThongKeGiaPaging" in request.url:
                print(request.url)
                body = dict(parse_qsl(request._body.decode('UTF-8')))
                FileAccessor.write_json("vietstock_sts_bodies.json", body)
    driver.close()
