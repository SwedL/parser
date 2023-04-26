import time
from telethon import TelegramClient, events, sync, connection
from telethon.tl.types import InputMessagesFilterPhotos

r_api = '15952889'
r_hash = '19d544ca657257dca2dcf7490980d6d1'
res = 0
username_lst = []

with TelegramClient('my', r_api, r_hash) as client:
    all_message = client.get_messages('https://t.me/Parsinger_Telethon_Test', filter=InputMessagesFilterPhotos, limit=100)
    for message in all_message:
        client.download_media(message, file='IMG/')

    time.sleep(5)



