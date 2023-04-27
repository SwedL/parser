import time
import aiofiles
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os


domain = 'https://parsinger.ru/asyncio/aiofile/2/'

async def write_file(session, url, name_img):
    async with aiofiles.open(f'images/{name_img}', mode='wb') as f:
        async with session.get(url) as response:
            async for x in response.content.iter_chunked(1024):
                await f.write(x)
        print(f'Изображение сохранено {name_img}')


async def main():
    url = 'https://parsinger.ru/asyncio/aiofile/2/index.html'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')

            url_pages = [domain + x["href"] for x in soup.find_all('a', class_='lnk_img')]
            img_link = []
            print(url_pages)
            for u in url_pages:
                async with session.get(u) as resp:
                    soup1 = BeautifulSoup(await resp.text(), 'lxml')
                    img_link.extend([k['src'] for k in soup1.find_all('img', class_='picture')])
            print(img_link)
            tasks = []
            for link in img_link:
                name_img = link.split('/')[6]
                print(name_img)
                task = asyncio.create_task(write_file(session, link, name_img))
                tasks.append(task)
            await asyncio.gather(*tasks)


start = time.perf_counter()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
print(f'Cохранено изображений {len(os.listdir("images/"))} за {round(time.perf_counter() - start, 3)} сек')


