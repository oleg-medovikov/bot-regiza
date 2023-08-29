from .base import metadata, database, engine
from .user import t_users
from .dict_orgs import t_dict_orgs
from .dict_mkb import t_dict_mkb
from .dict_doctor import t_dict_doctor
from .toxic_cases import t_toxic_cases
from .dict_obser import t_dict_obser
from .toxic_case_error import t_toxic_cases_errors
from .logi import t_logi
from .adress import t_adress
from .tokens import t_tokens

metadata.create_all(engine)

__all__ = [
    'metadata',
    'database',
    'engine',
    't_users',
    't_dict_orgs',
    't_dict_mkb',
    't_dict_doctor',
    't_toxic_cases',
    't_dict_obser',
    't_toxic_cases_errors',
    't_logi',
    't_adress',
    't_tokens',
]
