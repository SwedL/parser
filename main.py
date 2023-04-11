import json
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from tqdm import tqdm    # для красивой визуализации обработки


start_page = 'https://parsinger.ru/html/index1_page_1.html'
shema = "https://parsinger.ru/html/"
ua = UserAgent()
result_json = []


# функция приготовления супа по указанному URL
def resp(url: str) -> BeautifulSoup:
    fake_us = {'user-agent': ua.random}
    response = requests.get(url=url, headers=fake_us)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


# получаем все страницы категорий
categories = [shema + p['href'] for p in resp(start_page).find('div', 'nav_menu').find_all('a')]

# проходим циклом по всем категориям
for cat in tqdm(categories, ncols=80, desc='Processing'):
    pages_cat = [shema + p['href'] for p in resp(cat).find('div', 'pagen').find_all('a')]

    # проходим циклом по всем страницам текущей категории
    for page in pages_cat:
        soup = resp(page)
        items = soup.find_all('div', 'item')

        # получаем данные по каждой карточке товара
        for item in items:
            name = item.find('a', class_='name_item').text.strip()
            description = dict(map(lambda i: tuple(y.strip() for y in i.text.split(':')), item.find_all('li')))
            price = item.find('p', class_='price').text

            dict_data_item = {'Наименование': name}
            dict_data_item.update(description)
            dict_data_item.update({'Стоимость': price})

            # заносим в список словарь данных каждого товара
            result_json.append(dict_data_item)


# сериализация списка словарей в файл
with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(result_json, file, indent=4, ensure_ascii=False)











