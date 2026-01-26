import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch_page(session, url):
    async with session.get(url) as response:
        status = response.status
        html = await response.text()
        return status, html

async def parse_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    items = soup.find_all(attrs={"data-marker": "item"})
    for item in items:
        a_tag = item.find('a', href=True)
        if a_tag:
            links.append(a_tag['href'])
    return links

async def process_page(session, url):
    status, html = await fetch_page(session, url)
    if status == 200:
        links = await parse_links(html)
        print(f"URL: {url}")
        print(f"Найдено ссылок: {len(links)}")
    else:
        print(f"URL: {url} - Ошибка, статус: {status}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 40):
            url = f"https://www.avito.ru/moskva/odezhda_obuv_aksessuary/muzhskaya_odezhda-ASgBAgICAUTeAtgL?cd={i}&q=%D1%85%D1%83%D0%B4%D0%B8+diesel"
            tasks.append(process_page(session, url))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())