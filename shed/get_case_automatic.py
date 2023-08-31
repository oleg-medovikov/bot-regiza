from datetime import datetime, timedelta

from clas import User, Organization
from func import bot_send_text, toxic_get_cases, prepare_toxic_cases
from conf import MASTER


async def get_case_automatic():
    # берем список актуальных организаций
    ORGS = await Organization.get_org_list()
    START = datetime.now() - timedelta(days=25)
    END = datetime.now() + timedelta(days=1)
    USER = await User.get(MASTER)

    try:
        df = toxic_get_cases(
            START.strftime('%Y-%m-%d'),
            END.strftime('%Y-%m-%d'),
            ORGS
        )
    except Exception as e:
        return bot_send_text(str(e), int(USER.u_id))

    mess = f'Загружаю случаи с {START.strftime("%Y-%m-%d")}'
    mess += f' по {END.strftime("%Y-%m-%d")}'
    mess += f'\nРазмер датафрейма {len(df)}\n'

    count_add = 0
    count_cancel = 0

    for TC in await prepare_toxic_cases(df):
        try:
            await TC.add()
        except Exception as e:
            mess += str(e)
        else:
            # await ToxicCaseError.delete(TC.case_biz_key)
            if TC.is_cancelled:
                count_cancel += 1
            else:
                count_add += 1

    mess += f'Добавлено случаев: {count_add}\n'
    mess += f'Отмененные случаи: {count_cancel}\n'

    return bot_send_text(mess, int(USER.u_id))
