def find_flat(STRING: str) -> str:
    for part in STRING.split(','):
        for key in ['кв.', 'квартира']:
            if key in part.lower():
                return part
    return ''
