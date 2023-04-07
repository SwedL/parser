from bs4 import BeautifulSoup
import requests

url = 'https://parsinger.ru/html/index1_page_1.html'


def resp(url: str):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

soup = resp(url)
shema = 'https://parsinger.ru/html/'
total_cost = 0
temp = []

# страницы категорий товара
nav_menu = [shema + h['href'] for h in soup.find('div', 'nav_menu').find_all('a')]

#берем каждую категорию и выбираем все страницы категории (5 категорий - 5 страниц)
for cat in nav_menu:
    s1 = resp(cat)
    pages_items = [shema + t['href'] for t in s1.find('div', 'pagen').find_all('a')]

    #выбираем все ссылки страниц каждой категории (4 страницы на каждой категории)
    for page_item in pages_items:
        s2 = resp(page_item)
        temp = [shema+t['href'] for t in s2.find_all('a')][:4]

    #выбираем все ссылки на товары каждой страницы
    for item in temp:
        s3 = resp(item)
        links_item = [shema+d.a['href'] for d in s3.find_all('div', class_='sale_button')]

        #проходимся по каждой ссылке товара, получаем данные для расчёта
        for link in links_item:
            s4 = resp(link)
            price = int(s4.find('span', id='price').text.split()[0])
            in_stock = int(s4.find('span', id='in_stock').text.split()[-1])
            total_cost += price * in_stock


with open('answer', 'w', encoding='utf-8') as file:
    file.write(str(total_cost))

print(total_cost)
