from .base import metadata

from sqlalchemy import Table, Column, Integer, String, DateTime

t_users = Table(
    "users",
    metadata,
    Column('u_id', Integer),  # Идентификатор юзера в телеге
    Column('fio', String),  # ФИО юзера
    Column('org', String),  # Организация пользователя
    Column('role', String),  # профиль прав пользователя
    Column('date_create', DateTime),
    )
