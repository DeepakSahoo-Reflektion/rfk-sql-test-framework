import re

## TODO: empty file check also, i.e len(name) == 0
def is_sql_script(name = None):
    print('inside is_sql_script',name)
    if not name:
        raise ValueError('Name is not specified')

    r1 = re.findall(r"([^\s]+(\.(?i)(sql))$)", name)

    for pair in r1:
        return True
    return False

