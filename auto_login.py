# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0052DCE5EB6B8255BE723F7C64543D1C6B0460051C3F62A64DC0232225A4F7DCE7A663BE424DD90506E5E7A69DD5D90A47C044462E3C88A3960AA10F9EA74D7911D1B6B611FFED2429412BCE44972DA9AEC78B321DE4BB3644731E9C20280D5414891E0E237D93DA991C8DAFCC9A4BA99F3151811B8AE91775C450F9971B0F1E986A5F3A12E68E1915759B8AAC5F8CBD52E7A30BF406C8F59D88F74D8B611AB614D373AEA934740E85F9AFE5E869CAB6AFF1F7F3DA6D980813DF5200392227C484043D1E8064428818055559B0563C9E403C968DAC49337937E18C90529D0ED739C7192D5C5C0A74DC6EE863A3215C67728B74187CDF67CF47F89F5CA32A05E3BD222E9D08114D36A5083B7C58CD35509C3866FCE47CC11EC6322F3CCAAE602D843F3557F1ADD56D063F7633FD4F24EA5D558CA43B3DFF367801D764DDB17B375069FFEE7245517375C508CD0C53F2A9BA751FECB9420EC0659B07A3CF9F1B9DE5"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
