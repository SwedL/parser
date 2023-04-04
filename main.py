import requests


for i in range(1, 161):
    open_file = f'image{i}.jpg'
    url = f'https://parsinger.ru/img_download/img/ready/{i}.png'
    response = requests.get(url=url)
    with open(f'Foto/{open_file}', 'wb') as file:
        file.write(response.content)

