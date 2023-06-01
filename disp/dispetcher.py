from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from conf import TELEGRAM_TOKEN

import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logging.getLogger('schedule').propagate = False
logging.getLogger('schedule').addHandler(logging.NullHandler())


loop = asyncio.set_event_loop(asyncio.new_event_loop())
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
