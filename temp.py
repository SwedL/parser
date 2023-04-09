import requests
from bs4 import BeautifulSoup as bs
import lxml
import csv


def downoload_html(url):
    with open("file_html.txt", "w", encoding="utf-8-sig") as f:
        resp = requests.get(url)
        resp.encoding = "utf-8"
        f.write(resp.text)

    with open("file_html.txt", encoding="utf-8") as file:
        return file.read()


info = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Тип', 'Технология экрана', 'Материал корпуса',
        'Материал браслета',
        'Размер', 'Сайт производителя', 'Наличие', 'Цена', 'Старая цена', 'Ссылка на карточку с товаром']

url = "https://parsinger.ru/html/index1_page_1.html"

response = downoload_html(url)

soup = bs(response, "lxml")

categories = [el["href"] for el in soup.find("div", class_="nav_menu").find_all("a")]

with open("file_c.csv", "w", encoding='utf-8-sig', newline="") as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(info)
    sheme = "https://parsinger.ru/html/"

    url = sheme + categories[0]

    soup = bs(downoload_html(url), "lxml")

    list_pages = [el["href"] for el in soup.find("div", class_="pagen").find_all("a")]

    for slice_link in list_pages:
        url = sheme + slice_link
        soup = bs(downoload_html(url), "lxml")

        links = [el['href'] for el in soup.find("div", class_="item_card").find_all('a', class_="name_item")]

        for link in links:
            url = sheme + link

            soup_item = bs(downoload_html(url), "lxml")
            print(soup_item)
            list_rows = [soup_item.find('p', id='p_header').text.strip(),
                         soup_item.find('p', class_='article').text.split(':')[1]]
            list_rows += [el.text.split(':', 1)[1].strip() for el in
                          soup_item.find('ul', id='description').find_all('li')]
            list_rows += [soup_item.find('span', id=el).text.split(':')[-1].strip() for el in
                          ['in_stock', 'price', 'old_price']]
            list_rows.append(url)
            writer.writerow(list_rows)