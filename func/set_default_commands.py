from aiogram.types import BotCommand

dict_ = {
    "start": "Приветсвие",
    "meddoc": "Найти документ по его номеру",

}


async def set_default_commands(dp):
    commands = []

    for key, value in dict_.items():
        commands.append(
            BotCommand(command=key, description=value)
            )

    await dp.bot.set_my_commands(commands)
