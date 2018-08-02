import re
import logging

from common.const.vars import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def tables_in_query(sql_str):
    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql_str)
    lines = [line for line in q.splitlines() if not re.match("^\s*(--|#)", line)]
    q = " ".join([re.split("--|#", line)[0] for line in lines])
    tokens = re.split(r"[\s)(;]+", q)

    result = set()
    get_next = False
    for tok in tokens:
        if get_next:
            if tok.lower() not in ["", "select"]:
                result.add(tok)
            get_next = False
        get_next = tok.lower() in ["from", "join"]
    return result


def return_table_name(org_name):
    count_of_dots = org_name.count(DOT)
    new_name = org_name
    if count_of_dots == 0:
        new_name = TEST_UNDERSCORE + org_name
    elif count_of_dots == 1:
        new_name = org_name.split(DOT)[0] + '.test_' + org_name.split('.')[1]
    elif count_of_dots == 2:
        new_name = org_name.split(DOT)[0] + DOT + org_name.split(DOT)[1] + '.test_' + org_name.split(DOT)[2]
    else:
        logger.error('error during table name substitution')
        raise Exception('error during table name substitution')
    return new_name


def create_new_sql(org_sql):
    org_table_names = tables_in_query(org_sql)
    pair = {org_name: return_table_name(org_name) for org_name in org_table_names}
    new_sql = org_sql
    for k, v in pair.items():
        new_sql = new_sql.replace(k, v)
    return new_sql


def enrich_sql(org_sql):
    new_sql = create_new_sql(org_sql)
    QRY_TEMPLATE = """{org_sql} UNION {new_sql} MINUS {org_sql} INTERSECT {new_sql}""".format(org_sql=org_sql,
                                                                                              new_sql=new_sql)
    logger.info('sql_util:enrich_sql: EXIT with %s', QRY_TEMPLATE)
    return QRY_TEMPLATE