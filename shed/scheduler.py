import asyncio
import aioschedule

from clas import User
from func import bot_send_text
from conf import MASTER

from .get_case_automatic import get_case_automatic
from .process_adress_automatic import process_adress_automatic


async def scheduler():
    # aioschedule.every(1).minutes.do(test_send)
    # aioschedule.every(5).minutes.do(get_case_automatic)
    aioschedule.every(6).hours.do(get_case_automatic)
    aioschedule.every(6).hours.do(process_adress_automatic)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def test_send():
    USER = await User.get(MASTER)
    bot_send_text('Привет от шедулера!', int(USER.u_id))
