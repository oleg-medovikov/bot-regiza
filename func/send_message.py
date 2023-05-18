import requests
from conf import TELEGRAM_TOKEN


def bot_send_text(mess: str, chat_id: int):
    mess = mess.replace('_', ' ').replace('@', ' ').replace('&', ' ')

    send_text = 'https://api.telegram.org/bot' \
        + TELEGRAM_TOKEN \
        + '/sendMessage'
    data = {
            'chat_id': chat_id,
            'parse_mode': 'Markdown',
            'text': mess,
            }
    requests.get(send_text, data=data)


def bot_send_file(file, chat_id):

    with open(file, 'rb') as f:
        files = {
                'document': f
                }

        url = 'https://api.telegram.org/bot' \
            + TELEGRAM_TOKEN \
            + '/sendDocument'

        requests.post(url, data={
            "chat_id": chat_id
            }, files=files)
