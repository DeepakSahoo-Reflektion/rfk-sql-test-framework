import re
import logging
import subprocess

from common.const.vars import *

LOGGER = logging.getLogger(__name__)


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
        LOGGER.error('error during table name substitution')
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
    LOGGER.info('sql_util:enrich_sql: EXIT with %s', QRY_TEMPLATE)
    return QRY_TEMPLATE


def seg_exec_types(args):
    snowsql_command_queries = [arg for arg in args if arg.startswith('snowsql>')]
    snowsql_command_queries_without_prompt = [arg.split('snowsql>')[1] for arg in args if arg.startswith('snowsql>')]
    others = [item for item in args if item not in snowsql_command_queries]
    LOGGER.debug('sql_util:seg_exec_types with snowsql:- %s', snowsql_command_queries_without_prompt)
    LOGGER.debug('sql_util:seg_exec_types with Normal SQL:-%s', others)
    return snowsql_command_queries_without_prompt, others


def execute_snowsql_command(args):


    for arg in args:
        LOGGER.info('EXECUTING:----------- %s', arg)
        SNOW_SQL_TEMPLATE = "/Applications/SnowSQL.app/Contents/MacOS/snowsql -o exit_on_error=true -o log_level=DEBUG -q '{}'"
        SNOW_SQL_TEMPLATE = SNOW_SQL_TEMPLATE.format(arg)
        ret = subprocess.call(SNOW_SQL_TEMPLATE, shell=True)
        LOGGER.info('sql_util:execute_snowsql_command with return %s', ret)
