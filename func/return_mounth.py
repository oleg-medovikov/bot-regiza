from datetime import datetime, date
from calendar import monthrange


def return_mounth(DATE: 'datetime'):
    "Получение дат начала и конца в виде строк"
    days = monthrange(DATE.year, DATE.month)[1]
    return date(DATE.year, DATE.month, 1), \
        date(DATE.year, DATE.month, days)
