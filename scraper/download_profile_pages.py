import pandas as pd
from bs4 import BeautifulSoup
import os, time, random, configparser

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


config = configparser.ConfigParser()
config.read('../config.ini')
username = config['DEFAULT']['username']
password = config['DEFAULT']['password']


# Login to LinkedIn
def get_element(selector_type=By.CSS_SELECTOR, css_tag=""):
    return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((selector_type, css_tag)))


driver = Chrome("../driver/chromedriver.exe")
driver.get("https://www.linkedin.com/login")

username = get_element(By.CSS_SELECTOR, "input[name='session_key']")
password = get_element(By.CSS_SELECTOR, "input[name='session_password']")

username.clear()
password.clear()

username.send_keys(username)
password.send_keys(password)

submit = get_element(By.CSS_SELECTOR, "button[class='btn__primary--large from__button--floating']")
submit.click()

# Download profiles
profile_urls = []
with open("profile_urls.txt") as f:
    profile_urls = f.readlines()

# profile_urls = [url.rstrip('\n') for url in profile_urls]
profile_urls = [url.split('?')[0] for url in profile_urls]


def download_profile(urls):
    i = 1
    for url in urls:
        driver.get(url)
        time.sleep(random.randrange(10,30))
        with open(f"../profile_{i}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            i = i + 1

download_profile(profile_urls[:1])
driver.close()
