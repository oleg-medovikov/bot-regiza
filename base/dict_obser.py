from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, DateTime

t_dict_obser = Table(
    "dict_obser",
    metadata,
    Column('id', SmallInteger, primary_key=True),  # порядковый номер
    Column('obs_code', SmallInteger),  # код обсервейшена
    Column('obs_name', String),  # название обсервейшина
    Column('nsi_key',  SmallInteger),  # ключ справочника NSI
    Column('rpn_key', String),  # ключ системы РПН
    Column('value',   String),  # значение
    Column('date_update', DateTime),
)
