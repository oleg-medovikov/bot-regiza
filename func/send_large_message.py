from aiogram.utils.exceptions import MessageIsTooLong


async def send_large_message(message, MESS):
    "отправка длинного сообщения"

    try:
        await message.answer(MESS)
    except MessageIsTooLong:
        for x in range(0, len(MESS), 4096):
            await message.answer(MESS[x:x + 4096])
