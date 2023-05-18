from aiogram.types import BotCommand

dict_ = {
    "start": "Приветсвие",
    "admin_panel": "Панель настроек бота",

}


async def set_default_commands(dp):
    commands = []

    for key, value in dict_.items():
        commands.append(
            BotCommand(command=key, description=value)
            )

    await dp.bot.set_my_commands(commands)
