import re
import os
import codecs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


## TODO: empty file check also, i.e len(name) == 0
def is_sql_script(name = None):
    print('inside is_sql_script',name)
    if not name:
        raise ValueError('Name is not specified')

    r1 = re.findall(r"([^\s]+(\.(?i)(sql))$)", name)

    for pair in r1:
        return True
    return False

def get_input_sql_type(arg):
    if is_sql_script(arg):
        return 'sql_script'
    elif arg.startswith('$'):
        return 'statment_placeholder'
    else:
        return 'statement'

def generate_sql_for_asserts(sql):
    pass


## TODO: revisit this
def read_file(file_loc):
    if not file_loc or len(file_loc) == 0:
        logger.error('Invalid file location')
        raise Exception('invalid file location')
    try:
        logger.info('abs_file_path %s', file_loc)
        f = open(file_loc, 'r', encoding='utf-8')
    except FileNotFoundError:
        logger.error('File Not found')
        raise Exception('file not found')
    return f

