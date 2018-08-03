import re
import os
import logging
import configparser

from codecs import open

LOGGER = logging.getLogger(__name__)


def is_sql_script(name=None):
    LOGGER.debug('inside is_sql_script %s', name)
    if not name or len(name) == 0:
        LOGGER.error('is_sql_script name is not specified')
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
        LOGGER.error('read_file:Invalid file location')
        raise Exception('invalid file location')
    try:
        LOGGER.info('read_file:abs_file_path %s', file_loc)
        f = open(file_loc, 'r', encoding='utf-8')
    except FileNotFoundError:
        LOGGER.error('read_file:File Not found in the location %s', file_loc)
        raise Exception('file not found')
    return f


def get_file_ext(file_name):
    return os.path.splitext(file_name)[1]


def get_file_name_without_ext(file_name):
    return os.path.splitext(file_name)[0]


def read_value_from_ini_file(file_loc, key=None):
    if not file_loc or len(file_loc) == 0 or not key:
        LOGGER.error('read_file:Invalid file location')
        raise Exception('invalid file location')
    config = configparser.ConfigParser()
    value = None
    try:
        config.read(file_loc)
        value = (config['SQL'][key])
    except FileNotFoundError:
        LOGGER.error('read_file:File Not found in the location %s or key is not present %s', file_loc, key)
        raise Exception('file not found')
    except Exception:
        LOGGER.error('read_file:File Not found in the location %s or key is not present %s', file_loc, key)
        raise Exception('file not found')
    return value
