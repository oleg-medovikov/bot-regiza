def find_flat(STRING: str) -> str:
    for key in ['кв.', 'кв ', 'квартира']:
        if key in STRING.lower():
            return STRING.lower().rsplit(key)[-1].replace(' ', '')
    return ''
