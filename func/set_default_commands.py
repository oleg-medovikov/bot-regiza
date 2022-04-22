from aiogram.types import BotCommand

async def set_default_commands(dp):
    commands = [
        BotCommand(command="start",
            description="Приветсвие"),
        BotCommand(command="meddoc",
            description="Найти документ по его номеру"),
        ]

    await dp.bot.set_my_commands(commands)
