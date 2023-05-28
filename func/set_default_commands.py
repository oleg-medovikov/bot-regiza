from aiogram.types import BotCommand

dict_ = {
    "start": "Приветсвие",
    "file_get_toxic_cases": "Получить файл выгрузки за период",
    "statistic_panel": "Панель статистики и сводных отчетов",
    "admin_panel": "Панель настроек бота",

}


async def set_default_commands(dp):
    commands = []

    for key, value in dict_.items():
        commands.append(
            BotCommand(command=key, description=value)
            )

    await dp.bot.set_my_commands(commands)
