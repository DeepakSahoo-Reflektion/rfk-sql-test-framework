
def get_function_by_name(cls, fn_str, log_key=None):
    try:
        return getattr(cls, fn_str)
    except AttributeError as e:
        return None

## TODO: for git, fs or s3
def extract_loc_type(arg):
    return 'fs'

def extract_qry_from(args):
    if ':' not in args:
        return args
    return args.split(':')[1]