import asyncio
import aiohttp
from codetiming import Timer

#---------------------start block 1------------------------
urls = ["http://google.com",
        "http://yahoo.com",
        "http://apple.com",
        "http://microsoft.com",
        "https://habr.com/",
        "https://www.youtube.com/",
        "https://stepik.org/",
        "https://docs.python.org/",
        "https://stackoverflow.com/",
        "https://www.reg.ru/"]
#---------------------end block 1------------------------



#---------------------start block 2------------------------
async def main(url):
    with Timer(text=f"Затрачено времени на запрос: {{:.3f}} сек"):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print(resp.url)
#---------------------end block 2------------------------


async def run_tasks():
    tasks = [main(link) for link in urls]
    await asyncio.gather(*tasks)

#---------------------start block 3------------------------
if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_tasks())
#---------------------end block 3------------------------
