import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random


class Seller:
    def __init__(self, start_url: str):
        self.__start_url = start_url
        options = Options()
        options.add_argument("window-size=1920,1080")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.0.0 Safari/537.36"
        )
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=options)

    def __captcha_solver(self):
        try:
            trouble = self.driver.find_element(By.CLASS_NAME, "firewall-title").text
        except Exception:
            print("все окей")
        else:
            time.sleep(10)
        finally:
            time.sleep(1)
    
    def __input_name(self, name: str):
        self.driver.get(self.__start_url)
        self.__captcha_solver()
        block = self.driver.find_element(By.CLASS_NAME, "styles-module-input-Z0mvi")
        block.send_keys("худи", " diesel")
        time.sleep(1)
        search_btn = self.driver.find_element(By.CSS_SELECTOR, "#bx_search > div.index-button-hgorj > div > button")
        search_btn.click()
        time.sleep(1)
    
    def __input_path(self, path: str):
        pass

    def __scrap_cloth(self, name: str, brend: list[str], price: list[int], path: str):
        self.__input_name(name)

        """ last_num = self.driver.find_element(By.CSS_SELECTOR, "#app > div > buyer-pages-mfe-location > div > div > div > div.styles-singlePageWrapper-AYlq4 > div > div.index-center-J0kQo.index-center_withTitle-L0jpj.index-centerWide-kehGi.index-center_marginTop_1-txWnc > div.index-inner-cnvQJ.index-innerCatalog-F0YN1 > div.index-content-FRUkN > div.js-pages.pagination-pagination-vjzAT > nav > div.styles-module-breakpoint-rO7ka.styles-module-breakpoint_s-blCQ3.styles-module-breakpoint_m-aztfK.styles-module-breakpoint_l-dGC6R.styles-module-breakpoint_xl-UDmKH.styles-module-breakpoint_xxl-BhGLu.styles-module-breakpoint_xxxl-euFBe > ul > li.styles-module-listItem-PCOn2.styles-module-listItem_last-bC2vY.styles-module-listItem_notFirst-RiyoF").text
        last_num = int(last_num)
        print(last_num) """

    def scrap(self):
        self.__scrap_cloth('худи diesel', ['1'], [1], "1")
        time.sleep(100)
    

if __name__ == "__main__":
    start_url = "https://www.avito.ru/"
    seller = Seller(start_url)
    seller.scrap()



