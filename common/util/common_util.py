import logging
from common.const.vars import FS, COLON

LOGGER = logging.getLogger(__name__)


def get_function_by_name(cls, fn_str, log_key=None):
    try:
        return getattr(cls, fn_str)
    except AttributeError as e:
        LOGGER.error('common_util:get_function_be_name Attribute error', e.args)
        return None


def extract_qry_from(args):
    if COLON not in args:
        return args
    return args.split(COLON)[1]