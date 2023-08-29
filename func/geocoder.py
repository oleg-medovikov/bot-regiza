import requests
import json


def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)
    return results


def geocoder(ADR: str, TOKEN: str):
    "Проверяем адрес с помощью геокодера яндекса"

    ADR = 'санкт-петербург ' + ADR
    ADRESS = ADR.replace(' ', '+').replace('++', '')
    URL = "https://geocode-maps.yandex.ru/1.x?format=json&lang=ru_RU" \
        + f"&kind=house&geocode={ADRESS}&apikey={TOKEN.token}"

    req = requests.get(URL)

    if req.status_code != 200:
        raise ValueError('токен закончился')

    DATA = req.text

    DICT_KEYS = {
        'point': 'Point',
        'CountryName': 'CountryName',
        'text': 'text',
        'sity': 'AdministrativeAreaName',
        'street': 'ThoroughfareName',
        'house': 'PremiseNumber',
        'index': 'PostalCodeNumber',
            }
    DICT = {}
    DICT['error'] = False
    for key, value in DICT_KEYS.items():
        try:
            DICT[key] = find_values(value, DATA)[0]
        except IndexError:
            if key == 'index':
                DICT[key] = 0
            elif key == 'point':
                DICT[key] = {'pos': '0 0'}
            else:
                DICT[key] = ''
            DICT['error'] = True

    if DICT['sity'] != 'Санкт-Петербург':
        DICT['error'] = True

    return DICT
