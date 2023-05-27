from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
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
    o_303:           Optional[date]
    o_1101:          Optional[int]
    o_1103:          Optional[str]
    o_1104:          Optional[date]
    o_1105:          Optional[date]
    o_1106:          Optional[int]
    o_1107:          Optional[str]
    o_1108:          Optional[int]
    o_1109:          Optional[int]
    o_1110:          Optional[int]
    o_1111:          Optional[str]
    o_1112:          Optional[int]
    o_1113:          Optional[int]
    o_1114:          Optional[int]
    o_1115:          Optional[int]
    o_1116:          Optional[str]
    o_1117:          Optional[int]
    o_1118:          Optional[str]
    o_1119:          Optional[int]
    o_1123:          Optional[str]
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
