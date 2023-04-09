import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


shema = "https://parsinger.ru/html/index"


# функция приготовления супа по указанному URL
def resp(url: str):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')

    for category in tqdm(range(1, 6), desc='Сбор данных с карточек товаров...'):    # проходим циклом по всем категориям товаров

        for page in range(1, 5):    # проходим по всем страницам текущей категории
            url = shema + f'{str(category)}_page_{str(page)}.html'
            soup = resp(url)

            name = [x.text.strip() for x in soup.find_all('a', 'name_item')]
            description = [[x.split(':')[1].strip() for x in des.text.split('\n') if x] for des in soup.find_all('div', 'description')]
            price = [pr.text for pr in soup.find_all('p', 'price')]

            # создём строки отдельного товара (имя, описание, цена) из собранных списков имён описаний и цен
            for n, descr, p in zip(name, description, price):
                row = n, *descr, p
                writer.writerow(row)
