import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from aiohttp_socks import ChainProxyConnector
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent

domain = 'https://parsinger.ru/html/'


class Parser:
    def __init__(self, url):
        self.url = url
        self.result = 0
        self.category_lst = []
        self.pagen_lst = []
        self.urls_items = []
        self.made_params()

    def get_soup(self, url):
        resp = requests.get(url=url)
        return BeautifulSoup(resp.text, 'lxml')

    def get_urls_categories(self, soup):
        all_link = soup.find('div', class_='nav_menu').find_all('a')

        for cat in all_link:
            self.category_lst.append(domain + cat['href'])

    def get_urls_pages(self):
        for cat in self.category_lst:
            soup = self.get_soup(cat)
            for pagen in soup.find('div', class_='pagen').find_all('a'):
                self.pagen_lst.append(domain + pagen['href'])

    def get_urls_items(self):
        for u in self.pagen_lst:
            soup = self.get_soup(u)
            res = [domain + i.next_element['href'] for i in soup.find_all('div', class_='sale_button')]
            self.urls_items.extend(res)

    def made_params(self):
        soup = self.get_soup(self.url)
        self.get_urls_categories(soup)
        self.get_urls_pages()
        self.get_urls_items()
        self.made_asyncio()

    async def get_data(self, session, link):
        retry_options = ExponentialRetry(attempts=5)
        retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                                   start_timeout=0.5)
        async with retry_client.get(link) as response:
            if response.ok:
                resp = await response.text()
                soup = BeautifulSoup(resp, 'lxml')
                price = int(soup.find('span', id='price').text.split()[0])
                old_price = int(soup.find('span', id='old_price').text.split()[0])
                in_stock = int(soup.find('span', id='in_stock').text.split()[-1])
                print(price)
                self.result += (old_price - price) * in_stock

                # item_card = [x['href'] for x in soup.find_all('a', class_='name_item')]
                # for x in item_card:
                #     url2 = domain + x
                #     async with session.get(url=url2) as response2:
                #         resp2 = await response2.text()
                #         soup2 = BeautifulSoup(resp2, 'lxml')
                #         article = soup2.find('p', class_='article').text
                #         name = soup2.find('p', id='p_header').text
                #         price = soup2.find('span', id='price').text
                #         print(url2, price, article, name)


    async def main(self):
        ua = UserAgent()
        fake_ua = {'user-agent': ua.random}
        connector = ChainProxyConnector.from_urls(
            [
                'socks5://vvh2Ww:7trEfA@193.7.198.74:8000',
            ]
        )
        async with aiohttp.ClientSession(connector=connector, headers=fake_ua) as session:
            tasks = []
            for link in self.urls_items:
                task = asyncio.create_task(self.get_data(session, link))
                tasks.append(task)
            await asyncio.gather(*tasks)

    def made_asyncio(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.main())


url = 'https://parsinger.ru/html/index1_page_1.html'



p = Parser(url)

# print(p.pagen_lst)
# print(p.category_lst)
#print(p.urls_items)
print(p.result)

