from func import set_default_commands
from base import database


async def on_startup(dp):
    # запустим подключение к базе
    await database.connect()
    # это команды меню в телеграм боте
    await set_default_commands(dp)
    # Начинаем работу бота
    await dp.start_polling()
