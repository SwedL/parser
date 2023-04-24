import time
from telethon import TelegramClient, events, sync, connection


r_api = '15952889'
r_hash = '19d544ca657257dca2dcf7490980d6d1'
res = 0



with TelegramClient('my', r_api, r_hash) as client:
    all_message = client.get_messages('https://t.me/Parsinger_Telethon_Test')
    for message in all_message:
        res += int(message.message)
        print(message.message)
        if message.pinned:
            res3 = message.from_id.user_id
    print(res)
    print(res3)
    time.sleep(5)


