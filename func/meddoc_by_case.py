from conf import REGIZ_TOKEN
import requests, base64

HEADER = dict( Authorization = REGIZ_TOKEN)


def meddoc_by_case(MEDDOC_ID : int):
    """Делает запрос, чтобы прочитать привязанный файл по номеру"""

    URL = f"http://regiz.gorzdrav.spb.ru/FhirProxy2/fhir/DocumentReference/{str(MEDDOC_ID)}?mimeTypeOriginal=true&_format=json"
    try:
        req = requests.get(URL, headers=HEADER)
    except Exception as s:
        print(str(s))
        return f'Ошибка получения ответа от апи:\n {str(s)}'


    try:
        TYPE_DOCUMENT = req.json()['entry'][0]['resource']['content'][0]['attachment']['contentType']
    except:
        return 'Нет такого файла'
    else:
        if TYPE_DOCUMENT != 'text/plain':
            return 'Это не текстовый документ'
    try:
        STRING = req.json()['entry'][0]['resource']['content'][0]['attachment']['data']       
    except:
        return 'Нет файла'
    else:
        try:
            TEXT = base64.decodebytes( STRING.encode('utf-8')).decode('utf-16')
        except Exception as e:
            return f'мне не удалось прочитать файл:\n {str(s)}'
    
        else:
            return TEXT 
