from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from conf import TELEGRAM_TOKEN, PROXY_URL

import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('schedule').propagate = False
logging.getLogger('schedule').addHandler(logging.NullHandler())

bot = Bot(token=TELEGRAM_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot, storage=MemoryStorage())
