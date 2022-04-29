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
    import time
    import requests

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

    driver.get("https://fiintrade.vn/#")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'goldenLayout')))
    time.sleep(5)
    driver.find_element_by_class_name('login-button').click()
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'exampleInputEmail1')))
    driver.find_element_by_id('exampleInputEmail1').send_keys('conglethanh20@gmail.com')
    driver.find_element_by_id('exampleInputPassword1').send_keys('Hpcompap241')
    driver.find_element_by_xpath('//*[@id="home"]/form/fieldset/div[3]/button').click()
    time.sleep(10)
    # webdriver.
    # driver.get("https://market.fiintrade.vn/MarketInDepth/GetValuationSeriesV2?language=vi&Code=VNINDEX&TimeRange=AllTime&FromDate=&ToDate=")
    # cookies = driver.get_cookies()
    # FileAccessor.write_json("vietstock_cookies.json", cookies)
    # today = datetime.now()
    # from_time = today - timedelta(days=7)
    # to_time = today + timedelta(days=7)
    # driver.get("https://finance.vietstock.vn/lich-su-kien.htm?page=1&from={}&to={}&tab=1&group=13&exchange=-1".format(from_time.date(), to_time.date()))
    for request in driver.requests:
        if request.response:
            if "https://market.fiintrade.vn/MarketInDepth/GetValuationSeriesV2" in request.url:
                print(request.url)
                # body = dict(parse_qsl(request._body.decode('UTF-8')))
                FileAccessor.write_json("fiintrade_headers.json", dict(request.headers))
    driver.close()
