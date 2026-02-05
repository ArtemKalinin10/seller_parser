from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests, time



link = "https://www.avito.ru/all/odezhda_obuv_aksessuary/muzhskaya_odezhda/dzhinsy/true_religion-ASgBAgICA0TeAtgL4ALgC~SODoynzgE?cd=1&f=ASgBAQICA0TeAtgL4ALgC~SODoynzgEBQOK8DSTw0TTu0TQ&q=%D0%94%D0%B6%D0%B8%D0%BD%D1%81%D1%8B+True+Religion&s=104"


for i in range(100):
    requests.get(link)
""" driver = webdriver.Chrome()
driver.get(link)
time.sleep(1000)
 """
