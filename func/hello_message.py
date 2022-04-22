import time 

def hello_message(user) -> str:
    temp = int(time.strftime("%H"))
    hello =  {
     0   <= temp   < 6  :  'Доброй ночи, ',
     6   <= temp   < 11 :  'Доброе утро, ',
     11  <= temp   < 16 :  'Добрый день, ',
     16  <= temp   < 22 :  'Добрый вечер, ',
     22  <= temp   < 24 :  'Доброй ночи, '
            }[True] + str(user.first_name) + ' ' + str(user.last_name)

    text = f"""
    <b> {hello} </b> \n 
    Этот бот должен облегчить вашу работу"""

    return text
