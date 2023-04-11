# pars all products data on site https://parsinger.ru/html/index1_page_1.html
# and save it in json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import secrets
import json

# init final result list as global
final_result = []


def cooking_soup(url):
    """Cooking soup"""
    ua = UserAgent()
    cookie_value = secrets.token_hex(16)
    headers = {
        'user-agent': ua.random,
        'cookies': cookie_value
    }
    response = requests.get(url=url, headers=headers)
    response.encoding = 'UTF-8'
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_nav_menus():
    """Pars all nav_menu links for 'parser' function"""
    url = 'https://parsinger.ru/html/index1_page_1.html'
    soup = cooking_soup(url)
    pagen = [int(x.text) for x in soup.find('div', class_='pagen').find_all('a')][-1]
    href_links = [nav['href'].split('_')[0]
                  for nav in soup.find('div', class_='nav_menu').find_all('a')]
    parser(href_links, pagen)


def parser(href_links, pagen):
    """Get href links and pars all data, on all pages"""
    for nav in href_links:
        url = f'https://parsinger.ru/html/{nav}'

        for page in range(1, pagen + 1):
            soup = cooking_soup(f'{url}_page_{page}.html')
            # pars product names
            product_names = [name.text.strip() for name in soup.find_all('a', class_='name_item')]
            # pars descriptions info
            descriptions = [descr.text.strip().split('\n') for descr in soup.find_all('div', class_='description')]
            # pars info about prices
            prices = [price.text.strip() for price in soup.find_all('p', class_='price')]
            # transmits parsed data to 'create_json' function
            create_json(product_names, descriptions, prices)


def create_json(*args):
    """Create keys and values and save it in list"""
    # init local result list
    result_json = []
    # save data in result list
    for data in zip(*args):
        name, descr, price = data
        result_json.append({
          "Наименование": name,
          descr[0].split(':')[0]: [x.split(':')[1].strip() for x in descr][0],
          descr[1].split(':')[0]: [x.split(':')[1].strip() for x in descr][1],
          descr[2].split(':')[0]: [x.split(':')[1].strip() for x in descr][2],
          descr[3].split(':')[0]: [x.split(':')[1].strip() for x in descr][3],
          "Цена": price
        })
    final_result.extend(result_json)


def save_json():
    """get global variable 'final_result' and save all data as json"""
    with open('result.json', 'w', encoding='UTF-8') as output_file:
        json.dump(final_result, output_file, indent=4, ensure_ascii=False)


# main
if __name__ == '__main__':
    start = datetime.now()
    print("Process launched...")
    get_nav_menus()
    save_json()
    end = datetime.now()
    print(end - start)
    print("Operation complete. Data was saved successfully.")