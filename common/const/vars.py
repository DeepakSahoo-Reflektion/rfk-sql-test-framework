import os

# snowflake constants
# SNOWSQL_HOME = os.getenv('SNOWSQL_HOME')
# SNOWSQL_CMD = '%s/bin/snowsql' % SNOWSQL_HOME
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PWD = os.getenv('SNOWFLAKE_PWD')
SNOWFLAKE_ACC = os.getenv('SNOWFLAKE_ACC')
SNOWFLAKE = 'Snowflake'

# execution type constants
EXECUTE_ONE = 'execute-one'
EXECUTE_ALL = 'execute-all'

# configuration file constants
SHEET_NAME = 'sheet_name'
SHEET_DATA='sheet_data'
SQL_PATH = 'sql_path'
NAME = 'name'
SCRIPT_PATH = 'script_path'
BEFORE_ONCE = 'before_once'
BEFORE_EACH = 'before_each'
BEFORE_TEST = 'before_test'
AFTER_TEST = 'after_test'
AFTER_ONCE = 'after_once'
AFTER_EACH = 'after_each'
TESTS = 'tests'
ASSERTS = 'asserts'
EXPECTED = 'expected'
SQL = 'sql'
MESSAGE = 'message'
SQL_SCRIPT = 'sql_script'
CONFIG_FILE_NAME = 'config_file_name'

# test framework constants
STATUS_SUCCESS = 'Success'
STATUS_FAILURE = 'Failure'
CASE = 'case'
SHEET = 'sheet'
SUITE = 'suite'
ASSERT='assert'
XUNIT = 'xunit'
BDD = 'bdd'
GIT = 'git'
S3 = 's3'
FS = 'fs'
COLON = ':'
UNDERSCORE = '_'
TEST_UNDERSCORE = 'test_'
DOT = '.'
DOLLAR = '$'

#command line constants
EXEC_STRATEGY = 'exec_strategy'
LOC_TYPE = 'loc_type'
EXEC_TYPE = 'exec_type'
FILE_PATH_LOC = 'file_path_location'
FILE_EXT='file_ext'

# instance constants
SERVICE_INSTANCE = 'service_instance'
HANDLER_INSTANCE = 'handler_instance'
