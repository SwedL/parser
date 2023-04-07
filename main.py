import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

url = "https://parsinger.ru/table/5/index.html"

response = requests.get(url=url)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'lxml')
dict1 = {}

res = [[float(i) for i in x.text.split('\n')[1:-1]] for x in soup.find('div', 'main').find_all('tr')[1:]]

print(len(res))
print(res)
result = [0] * 15

for k in res:
    for key in range(1, 16):
        key_string = f'{key} column'
        dict1.setdefault(key_string, )









