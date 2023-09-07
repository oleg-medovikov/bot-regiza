from datetime import date

from clas import User, Adress, Token
from func import bot_send_text, geocoder, find_flat
from conf import MASTER


async def process_adress_automatic():
    USER = await User.get(MASTER)
    # берем список адресов
    LIST_ADRESS = await Adress.get_empty_adress()

    if len(LIST_ADRESS) == 0:
        mess = 'Нет новых адресов для проверки!'
        return bot_send_text(mess, int(USER.u_id))

    try:
        TOKEN = await Token.get()
    except ValueError:
        mess = 'Не осталось доступных токенов'
        return bot_send_text(mess, int(USER.u_id))

    for ADR in LIST_ADRESS:
        try:
            await Adress.get(ADR)
        except ValueError:
            pass
        else:
            continue

        while True:
            try:
                DICT = geocoder(ADR, TOKEN)
            except ValueError:
                TOKEN.end = True
                TOKEN.end_date = date.today()
                await TOKEN.update()
                try:
                    TOKEN = await Token.get()
                except ValueError:
                    mess = 'Не осталось доступных токенов'
                    return bot_send_text(mess, int(USER.u_id))
            else:
                TOKEN.count += 1
                await TOKEN.update()
                break

        try:
            ADRESS = Adress(**{
                'line':   ADR,
                'point':  [float(_) for _ in DICT['point']['pos'].split(' ')],
                'text':   DICT['text'],
                'street': DICT['street'],
                'house':  DICT['house'],
                'flat':   find_flat(ADR),
                'index':  DICT['index'],
                'error':  DICT['error'],
                })
        except:
            continue

        await ADRESS.add()

    mess = 'Закончил проверять адреса геокодером'
    return bot_send_text(mess, int(USER.u_id))
