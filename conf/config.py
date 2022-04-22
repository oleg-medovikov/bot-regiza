from starlette.config import Config

config = Config('.conf')

TELEGRAM_TOKEN = config('BOT_API', cast=str)
DATABASE_URL = config('DATABASE_URL', cast=str)
REGIZ_TOKEN= config('REGIZ_TOKEN', cast=str)
