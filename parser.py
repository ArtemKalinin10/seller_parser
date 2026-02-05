import time
import re
import json
import undetected_chromedriver as uc

from datetime import timedelta, datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By

class Seller:
    def __init__(self):
        
        self.MONTHS = {
            "января": 1,
            "февраля": 2,
            "марта": 3,
            "апреля": 4,
            "мая": 5,
            "июня": 6,
            "июля": 7,
            "августа": 8,
            "сентября": 9,
            "октября": 10,
            "ноября": 11,
            "декабря": 12
        }
        
        self.links = {}
        
        with open("clothes.json", 'r', encoding="utf-8") as file:
            data = json.load(file)
            res = {i: item for i, item in enumerate(data)}
        self.res = res
        
        
        options = uc.ChromeOptions()

        #options.add_argument("--headless=new")  # важно: new
        options.page_load_strategy = 'eager' 
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")

        self.driver = uc.Chrome(
            version_main=144,
            options=options
        )
    
    def _check_for_captcha(self, wait=0) -> bool:
        try:
            if wait:
                WebDriverWait(self.driver, wait).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "firewall-title"))
                )
            else:
                self.driver.find_element(By.CLASS_NAME, "firewall-title")
        except TimeoutException:
            return False
        except:
            return False
        return True

    
    
    def _scroll_to_bottom(self, pause=0.5, step=1200, max_scrolls=50):
        last_height = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
        total_height = self.driver.execute_script("return document.body.scrollHeight")

        scrolls = 0
        while last_height < total_height and scrolls < max_scrolls:
            self.driver.execute_script(f"window.scrollBy(0, {step});")
            time.sleep(pause)

            last_height = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            scrolls += 1
            
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        
    def _convert_time(self, date_str: str) -> datetime:
        now = datetime.now()
        date_str = date_str.lower().strip()

        try:
            if "сегодня" in date_str:
                time_part = re.search(r'(\d{1,2}:\d{2})', date_str).group(1)
                hour, minute = map(int, time_part.split(":"))
                return datetime(now.year, now.month, now.day, hour, minute)

            elif "вчера" in date_str:
                time_part = re.search(r'(\d{1,2}:\d{2})', date_str).group(1)
                hour, minute = map(int, time_part.split(":"))
                yesterday = now - timedelta(days=1)
                return datetime(yesterday.year, yesterday.month, yesterday.day, hour, minute)

            else:
                m = re.search(r'(\d{1,2}) (\w+) в (\d{1,2}:\d{2})', date_str)
                if not m:
                    raise ValueError(f"Невозможно распознать дату: {date_str}")
                day, month_str, time_part = m.groups()
                day = int(day)
                month = self.MONTHS.get(month_str)
                if not month:
                    raise ValueError(f"Неверный месяц: {month_str}")
                hour, minute = map(int, time_part.split(":"))
                year = now.year if (month < now.month or (month == now.month and day <= now.day)) else now.year - 1
                return datetime(year, month, day, hour, minute)
        except Exception as e:
            print(f"Ошибка при конвертации даты '{date_str}': {e}")
            return now
        
    def _get_text(self, selector: str, timeout=2, retries=3) -> str:
        tries = 0
        while tries < retries:
            try:
                return WebDriverWait(self.driver, timeout).until(
                    lambda d: d.find_element(By.CSS_SELECTOR, selector).text
                )
            except StaleElementReferenceException:
                tries += 1
                time.sleep(0.5)
        raise RuntimeError(f"Не удалось получить элемент {selector} из-за StaleElementReference")
    
    def _scrap_cloth(self, link: str) -> tuple:
        for attempt in range(3):
            try:
                self.driver.get(link)
                wait = WebDriverWait(self.driver, 1.5)

                price_el = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[itemprop="price"]'))
                )
                time_el = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-marker="item-view/item-date"]'))
                )
                id_el = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-marker="item-view/item-id"]'))
                )

                price = price_el.get_attribute("content")
                time_str = time_el.text
                cloth_id = id_el.text
                return time_str, price, cloth_id
                
            except (TimeoutException, StaleElementReferenceException) as e:
                print(f"Элементы не загрузились, пробуем снова ({attempt + 1}) - {type(e).__name__}")
                time.sleep(1)
                continue

        raise RuntimeError(f"Не удалось получить данные для {link} после 3 попыток")

    def _scrap_links(self, id: int):
        items = self.driver.find_elements(
            By.CSS_SELECTOR,
            '[data-marker="item"]:not(.items-itemsCarouselWidget-qzTW2 [data-marker="item"])'
        )
        
        links = [item.find_element(By.CSS_SELECTOR, '[data-marker="item-photo-sliderLink"]').get_attribute("href") 
                for item in items]

        links_per_cource = self.links.get(id, [])
        add_flag = bool(links_per_cource)
        res_links = []

        for link in links:
            time_str, price, cloth_id = self._scrap_cloth(link)
            time_dt = self._convert_time(time_str)
            
            if datetime.now() - time_dt > timedelta(days=7):
                break

            if not add_flag:
                links_per_cource.append({"link": link, "id": cloth_id, "time": time_dt, "price": price})
            else:
                if time_dt > links_per_cource[0]["time"] and cloth_id not in [i["id"] for i in links_per_cource]:
                    res_links.append({"link": link, "id": cloth_id, "time": time_dt, "price": price})
                else:
                    break

        if not add_flag:
            res_links = links_per_cource
        elif add_flag:
            links_per_cource = res_links + links_per_cource

        self.links[id] = links_per_cource

        for res_link in res_links:
            print(res_link)
        print(len(res_links))
        print(f"\n{'-' * 10}\n")

    
    def scrap(self):
        start = time.perf_counter()
        for index_cloth, item in self.res.items():
            self.driver.get(item["path"])
            while self._check_for_captcha(wait=1):
                print("Капча на главной странице, ждём...")
                self.driver.get(item["path"])
            self._scroll_to_bottom()
            self._scrap_links(index_cloth)

        end = time.perf_counter()
        print(end - start)
    
    def close(self):
        try:
            self.driver.quit()
        except Exception:
            pass
    
    

if __name__ == "__main__":
    seller = Seller()
    try:
        seller.scrap()
    finally:
        seller.close()

#обращаюсь в бд к последней шмотке и запоминаю ее дату
#позже и больше чем неделя дальше не смотрю
#как только все шмотки просмотрел обновляю бд