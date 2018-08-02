import logging
from common.const.vars import FS,COLON

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_function_by_name(cls, fn_str, log_key=None):
    try:
        return getattr(cls, fn_str)
    except AttributeError as e:
        logger.error('common_util:get_function_be_name Attribute error',e.args)
        return None

## TODO: for git, fs or s3
def extract_loc_type(arg):
    return FS

def extract_qry_from(args):
    if COLON not in args:
        return args
    return args.split(COLON)[1]