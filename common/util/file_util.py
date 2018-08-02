import re
import os
import logging

from codecs import open

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def is_sql_script(name=None):
    logger.debug('inside is_sql_script %s', name)
    if not name or len(name) == 0:
        logger.error('is_sql_script name is not specified')
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


# TODO: revisit this
def read_file(file_loc):
    if not file_loc or len(file_loc) == 0:
        logger.error('read_file:Invalid file location')
        raise Exception('invalid file location')
    try:
        logger.info('read_file:abs_file_path %s', file_loc)
        f = open(file_loc, 'r', encoding='utf-8')
    except FileNotFoundError:
        logger.error('read_file:File Not found in the location %s', file_loc)
        raise Exception('file not found')
    return f


def get_file_ext(file_name):
    return os.path.splitext(file_name)[1]
