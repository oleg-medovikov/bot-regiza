from datetime import datetime


def get_rpn_age(birthdate: str, o_303: datetime) -> int:
    "Равсчитываем коды возрастов по дате рождения"
    delta = (
        o_303 - datetime.strptime(birthdate, '%Y-%m-%d')
    ).days
    return {
        delta < 32:        100 + delta,  # меньше месяца
        32 < delta < 365:  delta // 30 * 100,  # до года
        364 < delta < 365*3: (100*(delta // 365) + (delta % 365) // 30)*100,
        365*3-1 < delta < 365*100: (delta // 365)*10000,
        365*100-1 < delta:  1010000,
    }.get(True, 0)
