import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


shema = "https://parsinger.ru/html/"
headers = ['Наименование',
           'Артикул',
           'Бренд',
           'Модель',
           'Наличие',
           'Цена',
           'Старая цена',
           'Ссылка на карточку с товаром'
           ]


# функция приготовления супа по указанному URL
def resp(url: str) -> BeautifulSoup:
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(headers)
    links_items = []

    # проходим по всем категориям
    for category in tqdm(range(1, 6), ncols=80, desc='Search all links'):

        # проходим по всем страницам категории и получаем все ссылки на предметы
        for page in range(1, 5):
            soup = resp(shema + f'index{category}_page_{str(page)}.html')
            links_items.extend([shema + i.find('a')['href'] for i in soup.find_all('div', 'img_box')])

    # проходим по всем ссылкам и собираем необходимые данные
    for link in tqdm(links_items, ncols=80, desc=' Read data items'):
        soup = resp(link)

        name = soup.find('p', id='p_header').text
        article = soup.find('p', class_='article').text.split()[1]
        description = [i.text.split(': ')[1] for i in soup.find('div', 'description').find_all('li')[:2]]
        in_stock = soup.find('span', id='in_stock').text.split()[2]
        price = soup.find('span', id='price').text
        old_price = soup.find('span', id='old_price').text

        # создаём строку с данными и записываем в файл
        row = name, article, *description, in_stock, price, old_price, link
        writer.writerow(row)
