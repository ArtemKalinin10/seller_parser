import time
import re
import sqlite3
import undetected_chromedriver as uc
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


DB_PATH = "resell.db"


class Seller:
    """
    A class to scrape items from Avito based on saved subscriptions in a SQLite database.

    Attributes:
        conn (sqlite3.Connection): SQLite connection object.
        cur (sqlite3.Cursor): SQLite cursor object.
        MONTHS (dict): Mapping of Russian month names to their numerical values.
        driver (uc.Chrome): Undetected Chrome WebDriver instance.
    """

    def __init__(self):
        """
        Initializes the Seller instance, sets up the database connection and WebDriver.
        """
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

        # Russian month names mapping
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

        # Setup Chrome WebDriver options
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = uc.Chrome(options=options, version_main=144)

    # ------------------

    def correct_link(self, link: str) -> bool:
        """
        Checks if the provided link is valid by verifying region and sort order.

        Args:
            link (str): URL of the subscription page.

        Returns:
            bool: True if region is "all regions" and sort is "by date", False otherwise.
        """
        try:
            self.driver.get(link)
            wait = WebDriverWait(self.driver, 5)

            region = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-marker="search-form/change-location"]')
                )
            ).text.strip().lower()

            sort_title = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-marker="sort/title"]')
                )
            ).text.strip().lower()

            if region == "во всех регионах" and sort_title == "по дате":
                return True

            return False

        except Exception:
            return False

    # ------------------

    def _convert_time(self, text: str) -> datetime:
        """
        Converts Russian date strings from the site into a Python datetime object.

        Args:
            text (str): Date string (e.g., "Сегодня в 14:35", "5 февраля в 13:00").

        Returns:
            datetime: Corresponding datetime object.
        """
        now = datetime.now()
        text = text.lower()

        try:
            if "сегодня" in text:
                h, m = map(int, re.search(r"(\d{1,2}:\d{2})", text).group(1).split(":"))
                return datetime(now.year, now.month, now.day, h, m)

            if "вчера" in text:
                h, m = map(int, re.search(r"(\d{1,2}:\d{2})", text).group(1).split(":"))
                d = now - timedelta(days=1)
                return datetime(d.year, d.month, d.day, h, m)

            d, m_txt, t = re.search(r"(\d{1,2}) (\w+) в (\d{1,2}:\d{2})", text).groups()
            m = self.MONTHS[m_txt]
            h, mi = map(int, t.split(":"))
            y = now.year if m <= now.month else now.year - 1

            return datetime(y, m, int(d), h, mi)

        except Exception:
            return now

    # ------------------

    def _item_exists(self, avito_id: str) -> bool:
        """
        Checks if an item already exists in the database.

        Args:
            avito_id (str): Unique Avito item ID.

        Returns:
            bool: True if item exists, False otherwise.
        """
        self.cur.execute("SELECT 1 FROM items WHERE avito_id = ?", (avito_id,))
        return self.cur.fetchone() is not None

    # ------------------

    def _scrap_item(self, link: str):
        """
        Scrapes a single item page for its details: time, price, ID, and image.

        Args:
            link (str): URL of the item page.

        Returns:
            tuple: (time_str, price, avito_id, img_url) or (None, None, None, None) if failed.
        """
        for _ in range(4):
            try:
                self.driver.get(link)
                wait = WebDriverWait(self.driver, 5)

                price = wait.until(
                    lambda d: d.find_element(By.CSS_SELECTOR, '[itemprop="price"]')
                ).get_attribute("content")

                time_str = wait.until(
                    lambda d: d.find_element(By.CSS_SELECTOR, '[data-marker="item-view/item-date"]')
                ).text

                avito_id = wait.until(
                    lambda d: d.find_element(By.CSS_SELECTOR, '[data-marker="item-view/item-id"]')
                ).text

                try:
                    img = self.driver.find_element(
                        By.CLASS_NAME, 'desktop-1ky5g7j'
                    ).get_attribute("src")
                except Exception:
                    img = None

                return time_str, int(price), avito_id, img

            except (TimeoutException, StaleElementReferenceException):
                time.sleep(1)

        return None, None, None, None

    # ------------------

    def scrap(self):
        """
        Main scraping function that iterates over all subscriptions,
        collects item links excluding carousel links, and inserts new items into the database.
        """
        self.cur.execute("SELECT * FROM subscriptions")
        subs = self.cur.fetchall()

        for sub in subs:
            print("🔍", sub["query"])

            self.driver.get(sub["url"])
            time.sleep(2)

            # Only select links NOT inside the itemsCarousel
            elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                '[data-marker="item-photo-sliderLink"]:not([data-marker="itemsCarousel"] [data-marker="item-photo-sliderLink"])'
            )

            links = []

            for el in elements:
                try:
                    href = el.get_attribute("href")
                    if href:
                        links.append(href)
                except StaleElementReferenceException:
                    continue

            for link in links:
                time_str, price, avito_id, img = self._scrap_item(link)

                if not avito_id:
                    continue

                if self._item_exists(avito_id):
                    break  # ❗ preserve old logic

                created_at = self._convert_time(time_str)

                self.cur.execute(
                    """
                    INSERT INTO items (
                        avito_id,
                        url,
                        price,
                        created_at,
                        query_name,
                        image_url
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (avito_id, link, price, created_at, sub["query"], img)
                )

                self.conn.commit()
                print("🆕 NEW:", link)

    # ------------------

    def close(self):
        """
        Closes the WebDriver and the database connection safely.
        """
        try:
            self.driver.quit()
        except Exception:
            pass

        self.conn.close()
