
def get_function_by_name(cls, fn_str, log_key=None):
    try:
        return getattr(cls, fn_str)
    except AttributeError as e:
        return None