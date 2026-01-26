import requests
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Seller:
    def __init__(self, start_url: str):
        self.__start_url = start_url
        self.links = []
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
        block.click()

        actions = ActionChains(self.driver)
        actions.move_to_element(block)
        actions.click()
        actions.send_keys(name)
        actions.perform()

        time.sleep(1)
        search_btn = self.driver.find_element(By.CSS_SELECTOR, "#bx_search > div.index-button-hgorj > div > button")
        search_btn.click()
        time.sleep(1)
    
    def __odezhda_obuv_aksessuary(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="category[1000037]"]')
        btn.click()

    def __muzhskaya_odezhda(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="category[1000266]"]')
        btn.click()
    
    def __kofty_i_futbolki(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="category[1000799]"]')
        btn.click()
    
    def __dzhinsy(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="category[1000797]"]')
        btn.click()
    
    def __sumki_ryukzaki_i_chemodany(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="category[31068]"]')
        btn.click()
    
    def __ryukzaki(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="category[31072]"]')
        btn.click()
    
    def __sumki(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="category[31071]"]')
        btn.click()
    
    def __input_path(self, path: str):
        for i in path.split('/'):
            match i:
                case "odezhda_obuv_aksessuary":
                    self.__odezhda_obuv_aksessuary()
                case "muzhskaya_odezhda":
                    self.__muzhskaya_odezhda()
                case "dzhinsy":
                    self.__dzhinsy()
                case "kofty_i_futbolki":
                    self.__kofty_i_futbolki()
                case "sumki_ryukzaki_i_chemodany":
                    self.__sumki_ryukzaki_i_chemodany()
                case "ryukzaki":
                    self.__ryukzaki()
                case "sumki":
                    self.__sumki()
            time.sleep(2)

    def __set_quality(self):
        good = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="params[110385]/checkbox/431223"]').click()
        normal = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="params[110385]/checkbox/431224"]').click()
        time.sleep(1)

    def __set_brends(self, brends: list[str]):

        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="params[115634]/show-button"]')
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()
        time.sleep(1)
        search = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="params[115634]/multiselect-search/input/input"]')
        for brend in brends:
            search.send_keys(brend)
            time.sleep(1.5)
            this_brend = self.driver.find_elements(By.CLASS_NAME, "multi-select-search-checkboxWrapper-DEBZH")
            for this in this_brend:
                if brend.strip() in this.text:
                    this_brend = this
                    break
            this_brend.click()
            time.sleep(1)
            clear_btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="params[115634]/multiselect-search/input/clear"]')
            clear_btn.click()

        
    def __set_prices(self, price: list[int]):
        first, second = price

        first_btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="price-from/input"]')
        second_btn = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="price-to/input"]')
        time.sleep(1)
        for char in str(int(first * 0.8)):
            first_btn.send_keys(char)
            time.sleep(0.2)
        
        for char in str(second):
            second_btn.send_keys(char)
            time.sleep(0.2)
        
        time.sleep(1)

    def __confirm_settings(self):
        self.driver.find_element(By.CSS_SELECTOR, '[data-marker="search-filters/submit-button"]').click()

    def __scrap_cloth(self, name: str, brends: list[str], price: list[int], path: str):
        self.__input_name(name)
        self.__input_path(path)
        self.__set_quality()
        self.__set_brends(brends)
        self.__set_prices(price)
        self.__confirm_settings()

        time.sleep(3)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.last_number = self.driver.find_elements(By.CLASS_NAME, "styles-module-text-Z0vDE")[-1].text
        self.last_number = int(self.last_number)
        self.current_page = 1
    
    def __scrap_all_clothes(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        while self.current_page <= self.last_number:
            print(self.current_page)
            items = self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, '[data-marker="item-photo-sliderLink"]').get_attribute("href")
                self.links.append(link)
            if "&p=" in self.driver.current_url:
                gp = re.match(r"(.+p=)(\d+)(.+)", self.driver.current_url).groups()
                next_link = gp[0] + str(int(gp[1]) + 1) + gp[2]
            else:
                gp = re.match(r"(.+)(q=.+)", self.driver.current_url).groups()
                next_link = gp[0] + "p=2&" + gp[1]
            self.current_page += 1
            if self.current_page > self.last_number:
                break
            self.driver.get(next_link)
            time.sleep(2)
        print(len(self.links))

        

    def scrap(self):
        self.__scrap_cloth("Худи Diesel", ["Diesel"], [7000, 12000], "odezhda_obuv_aksessuary/muzhskaya_odezhda/kofty_i_futbolki")
        self.__scrap_all_clothes()
        time.sleep(1000)
    

if __name__ == "__main__":
    start_url = "https://www.avito.ru/"
    seller = Seller(start_url)
    seller.scrap()