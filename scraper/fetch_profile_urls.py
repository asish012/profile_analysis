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

output_file = "profile_urls_analyst.txt"
search_key = "data scientist"

driver = Chrome("../driver/chromedriver.exe")
driver.get("https://www.linkedin.com/login")


def get_element(selector_type=By.CSS_SELECTOR, css_tag=""):
    return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((selector_type, css_tag)))


username = get_element(By.CSS_SELECTOR, "input[name='session_key']")
password = get_element(By.CSS_SELECTOR, "input[name='session_password']")

username.clear()
password.clear()

username.send_keys(username)
password.send_keys(password)

submit = get_element(By.CSS_SELECTOR, "button[class='btn__primary--large from__button--floating']")
submit.click()


search = get_element(By.CSS_SELECTOR, "button[class='search-global-typeahead__collapsed-search-button']")
# search = get_element(By.CSS_SELECTOR, "input[class='search-global-typeahead__input always-show-placeholder']") # fullscreen mode
search.click()

search_text = get_element(By.CSS_SELECTOR, "input[class='search-global-typeahead__input always-show-placeholder']")
search_text.send_keys(search_key)
search_text.send_keys(Keys.ENTER)

try:
    people = get_element(By.XPATH, "//button[@aria-label='People']")
    people.click()
except:
    people = get_element(By.XPATH, "//a[contains(text(), 'See all people results')]")
    people.click()


# Collect 1000 linkedin profile links
try:
    i = 0
    while i <= 500:

        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, features="lxml")
        profile_urls = soup.find_all("li", {"class": "reusable-search__result-container"})

        urls = []
        for li in profile_urls:
            url = li.find("a", {"class": "app-aware-link"})["href"]
            if 'search/result' not in url:
                urls.append(url)
                # print(f"{i}: {url}")
                i = i+1

        # write collected profile urls
        with open(output_file, "a") as f:
            f.write('\n'.join(urls))
            f.write('\n')

        # wait some time
        time.sleep(random.randrange(10, 30))

        # scroll and go to the next page
        driver.execute_script("window.scrollTo(0, 4000)")
        next = get_element(By.XPATH, "//button[@aria-label='Next']")
        next.click()
except:
    driver.close()

driver.close()
