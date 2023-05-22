from pydantic import BaseModel
from datetime import datetime, date

from base import database, t_toxic_cases


class ToxicCase (BaseModel):
    case_biz_key:    int
    org_id:          int
    history_number:  str
    sex:             bool
    age:             int
    mkb_id:          int
    diagnoz_date:    datetime
    doc_smo:         int
    doc_md:          int
    o_303:           date
    o_1101:          int
    o_1103:          str
    o_1104:          date
    o_1105:          date
    o_1106:          int
    o_1107:          str
    o_1108:          int
    o_1109:          int
    o_1110:          int
    o_1111:          str
    o_1112:          int
    o_1113:          int
    o_1114:          int
    o_1115:          int
    o_1116:          str
    o_1117:          int
    o_1118:          str
    o_1119:          int
    o_1123:          str
    errors:          str

    async def add(self):
        # проверяем наличие по case_biz_key
        query = t_toxic_cases.select(
            t_toxic_cases.c.case_biz_key == self.case_biz_key
        )
        res = await database.fetch_one(query)

        if res is None:
            query = t_toxic_cases.insert().values(self.dict())
        else:
            query = t_toxic_cases.update()\
                .where(t_toxic_cases.c.case_biz_key == self.case_biz_key)\
                .values(self.dict())

        await database.execute(query)
