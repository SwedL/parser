from bs4 import BeautifulSoup
import requests

url = 'https://parsinger.ru/html/index3_page_1.html'

response = requests.get(url=url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')
shuma = 'https://parsinger.ru/html/'
pagin = [shuma+t['href'] for t in soup.find('div', 'pagen').find_all('a')]

#print(soup)

res_art = []

link_item = []
for p in pagin:
    resp = requests.get(url=p)
    resp.encoding = 'utf-8'
    s = BeautifulSoup(resp.text, 'lxml')
    [link_item.append(shuma+link.find('a')['href']) for link in s.find_all('div', class_='img_box')]

#print(link_item)

for item in link_item:
    resp1 = requests.get(url=item)
    resp1.encoding = 'utf-8'
    soup1 = BeautifulSoup(resp1.text, 'lxml')
    res_art.append(int(soup1.find('p', 'article').text.split()[-1]))

print(sum(res_art))




