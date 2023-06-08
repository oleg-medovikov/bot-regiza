import asyncio
import aioschedule
from datetime import datetime, timedelta

from clas import User, Organization, ToxicCase, ToxicCaseError
from func import bot_send_text, toxic_get_cases, prepare_toxic_cases
from conf import MASTER


async def scheduler():
    # aioschedule.every(1).minutes.do(test_send)
    # aioschedule.every(5).minutes.do(get_case_automatic)
    aioschedule.every(6).hours.do(get_case_automatic)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def test_send():
    USER = await User.get(MASTER)
    bot_send_text('Привет от шедулера!', int(USER.u_id))


async def get_case_automatic():
    # берем список актуальных организаций
    ORGS = await Organization.get_org_list()
    START = datetime.now() - timedelta(days=20)
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

    mess = f'Размер датафрейма {len(df)} \n'

    df_is_canselled = df.loc[df['case_is_cancelled'] == '1']

    count = 0
    for case_biz_key in df_is_canselled['case_biz_key'].unique():
        try:
            await ToxicCase.delete(case_biz_key)
        except Exception as e:
            mess += str(e)
        else:
            count += 1
    mess += f'удалено отмененных случаев: {count}\n'

    df = df.loc[df['case_is_cancelled'] == '0']
    count = 0
    for TC in await prepare_toxic_cases(df):
        try:
            await TC.add()
        except Exception as e:
            mess += str(e)
        else:
            await ToxicCaseError.delete(TC.case_biz_key)
            count += 1

    mess += f'обработано {count} случаев\n'
    return bot_send_text(mess, int(USER.u_id))
