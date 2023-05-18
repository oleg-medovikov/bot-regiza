from aiogram.utils.exceptions import MessageToDeleteNotFound


async def delete_message(message):
    "удаление сообщения с обработкой исключения"

    try:
        await message.delete()
    except MessageToDeleteNotFound:
        pass
