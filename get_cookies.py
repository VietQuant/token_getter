import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import settings
import os
logging.basicConfig(format='%(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

URLS = ["https://myaccount.fireant.vn/"]

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def login(driver, url, username, password):
    driver.get(url)
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'mvClientID')))
    id_elem = driver.find_element_by_id("mvClientID")
    id_elem.send_keys(username)
    pass_elem = driver.find_element_by_id("mvPassword")
    pass_elem.send_keys(password)
    captcha_elem = driver.find_element_by_id("mainCaptcha")
    captcha = ''.join(captcha_elem.text.split(' '))
    captcha_text_elem = driver.find_element_by_id("securitycode")
    captcha_text_elem.send_keys(captcha)
    captcha_text_elem.send_keys(Keys.RETURN)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@onclick,'cancel')]")))
        driver.find_element_by_xpath("//button[contains(@onclick,'cancel')]").click()
    except Exception as e:
        logging.warning("{} khong click nut Huy duoc".format(e))


if __name__ == '__main__':
    from rework_backtrader.utils.file_accessor import FileAccessor
    from datetime import datetime, timedelta

    remote = os.getenv("REMOTE_CHROME", None)
    if remote:
        driver = webdriver.Remote(remote, DesiredCapabilities.CHROME, options=set_chrome_options())
    else:
        driver = webdriver.Chrome(executable_path="drivers/chromedriver", options=set_chrome_options())
    driver.get("https://myaccount.fireant.vn")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-primary')))
    driver.find_element_by_class_name("btn-primary").click()
    username = driver.find_element_by_id("username")
    username.send_keys("doantvinh@gmail.com")
    password = driver.find_element_by_id("password")
    password.send_keys("Vietquant001")
    driver.find_element_by_class_name("btn-primary").click()
    driver.get("https://www.fireant.vn/App/#/company-data/VNM")
    driver.get("https://svr1.fireant.vn/api/Data/Markets/Bars?symbol=VNM&resolution=1&startDate={}&endDate={}".format(
                                        (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
                                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ))
    cookies = driver.get_cookies()
    FileAccessor.write_json("cookies.json", cookies)
    driver.close()
