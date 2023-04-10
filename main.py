import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


start_page = 'https://parsinger.ru/html/index3_page_1.html'    # категория мыши
shema = "https://parsinger.ru/html/"


# функция приготовления супа по указанному URL
def resp(url: str) -> BeautifulSoup:
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')

# получаем все страницы категории товара
pages = [shema + p['href'] for p in resp(start_page).find('div', 'pagen').find_all('a')]
res_data = []

for page in pages:
    soup = resp(page)
    data_items = soup.find_all('div', 'item')
    print(data_items)
    print()










