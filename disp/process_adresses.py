from .dispetcher import dp
from aiogram import types
from datetime import date

from func import delete_message, geocoder, find_flat
from clas import User, Log, Adress, Token


@dp.message_handler(commands=['process_adresses'])
async def process_adresses(message: types.Message):
    """проверяем адреса через геокодер яндекса"""
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        await Log.add(message['from']['id'], 1)
        return await message.answer(
            "Вы не являетесь админом",
            parse_mode='html'
            )

    await Log.add(message['from']['id'], 28)

    # берем список адресов
    LIST_ADRESS = await Adress.get_empty_adress()

    if len(LIST_ADRESS) == 0:
        mess = 'Нет новых адресов для обработки'
        return await message.answer(mess, parse_mode='Markdown')

    try:
        TOKEN = await Token.get()
    except ValueError:
        mess = 'Не осталось доступных токенов'
        return await message.answer(mess, parse_mode='Markdown')

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
                    return await message.answer(mess, parse_mode='Markdown')
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
        except Exception as e:
            print(str(e))
            print(ADR)
            print(DICT)
            continue

        await ADRESS.add()

    mess = 'Закончил!'
    return await message.answer(mess, parse_mode='Markdown')
