import json
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from tqdm import tqdm    # для красивой визуализации обработки


start_page = 'https://parsinger.ru/html/index3_page_1.html'    # выбираем категорию "мыши"
shema = "https://parsinger.ru/html/"
category = 'mouse'
ua = UserAgent()
result_list = []


# функция приготовления супа по указанному URL
def resp(url: str) -> BeautifulSoup:
    fake_us = {'user-agent': ua.random}
    response = requests.get(url=url, headers=fake_us)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


# получаем все страницы категорий
pages_mouse = [shema + p['href'] for p in resp(start_page).find('div', 'pagen').find_all('a')]
items_links = []

# проходим циклом по всем страницам выбранной категории и собираем все ссылки на каждую позицию
for page in tqdm(pages_mouse, ncols=80, desc='Search all links'):
    soup1 = resp(page)
    items_links.extend([shema + i.find('a')['href'] for i in soup1.find_all('div', 'sale_button')])

# проходим циклом по каждой ссылке позиции и получаем её данные
for link in tqdm(items_links, ncols=80, desc='Processing'):
    soup2 = resp(link)

    # создаём словарь с данными товара
    dict_data_item = {
        "categories": category,
        "name": soup2.find('div', 'description').find('p').text,
        "article": soup2.find('div', 'description').find('p', class_='article').text.split(':')[1].strip(),
        "description": dict(map(lambda desc: (desc['id'], desc.text.split(':')[1].strip()), soup2.find_all('li'))),
        "count": soup2.find('span', id='in_stock').text.split(':')[1].strip(),
        "price": soup2.find('span', id='price').text,
        "old_price": soup2.find('span', id='old_price').text,
        "link": link,
        }

    # добавляем словарь в результирующий список
    result_list.append(dict_data_item)


# сериализация списка словарей в файл
with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(result_list, file, indent=4, ensure_ascii=False)











