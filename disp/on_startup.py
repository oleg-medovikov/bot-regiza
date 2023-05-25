from func import set_default_commands
from base import database
from aiogram.utils.exceptions import NetworkError

import asyncio


async def on_startup(dp):
    # запустим подключение к базе
    await database.connect()
    # это команды меню в телеграм боте
    await set_default_commands(dp)
    while True:
        try:
            await dp.start_polling()
        except NetworkError:
            # print(str(e))
            asyncio.sleep(5)
