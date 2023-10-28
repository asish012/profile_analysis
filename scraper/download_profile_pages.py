import pandas as pd
from bs4 import BeautifulSoup
import os, time, random, configparser

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import codecs
import re


config = configparser.ConfigParser()
config.read('../config.ini')
lusername = config['DEFAULT']['username']
lpassword = config['DEFAULT']['password']


# Login to LinkedIn
def get_element(selector_type=By.CSS_SELECTOR, css_tag=""):
    return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((selector_type, css_tag)))


# driver = Chrome("../driver/chromedriver")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.linkedin.com/login")

username = get_element(By.CSS_SELECTOR, "input[name='session_key']")
password = get_element(By.CSS_SELECTOR, "input[name='session_password']")

username.clear()
password.clear()

username.send_keys(lusername)
password.send_keys(lpassword)

submit = get_element(By.CSS_SELECTOR, "button[class='btn__primary--large from__button--floating']")
submit.click()

# Download profiles
profile_urls = []
with open("profile_urls.txt") as f:
    profile_urls = f.readlines()

# profile_urls = [url.rstrip('\n') for url in profile_urls]
# profile_urls = [url.split('?')[0] for url in profile_urls]


def download_profile(urls):
    i = 1
    for url in urls:
        # Download profile
        driver.get(url)
        time.sleep(random.randrange(10,30))
        with open(f"../profile_html/profile_{i}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        # Download experience
        driver.get(url+'details/experience/')
        time.sleep(random.randrange(10,30))
        with open(f"../profile_html/profile_{i}_experience.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        i = i + 1

download_profile(profile_urls)
driver.close()
