from common.db.connection import ConnectionFactory
from engine.executor.executor_factory import *
from engine.resolver.fs_resolver import *
from engine.parser.json_parser import *

### for testing the snowflake_connection
# conn = ConnectionFactory.get_connection('Snowflake')
#
# cur = conn.cursor()
# row = cur.execute('SELECT * FROM TEST.EM.be_workflow_step1_inventory_trigger_rows')
# row_data = row.fetchall()
#
# if row is not None:
#     headers = [i[0] for i in row.description]
#     print(headers)
#
# cur.close()
# conn.commit()
# conn.close()


### testing the service module
# try:
#
#     db_service = DBService()
#     x = db_service.serve('SELECT * FROM TEST.EM.be_workflow_step1_inventory_trigger_rows')
#     print(x)
# finally:
#     print('closing connection.....')
#     db_service.close()


## json parser test
# file = FileLocPathResolver().resolve('/Users/deepak/PycharmProjects/rfk-sql-test-framework/sample_config_file.json')
# data = JsonParser().parse(file)
# print(data)

# testing the executor_factory
# executor = ExecutorFactory.get_executor('XUnitStyle')
# print(executor)
# print(dir(executor))

## testing the executor
# file = FileLocPathResolver().resolve('/Users/deepak/PycharmProjects/rfk-sql-test-framework/sample_config_file.json')
# test_sheet = JsonParser().parse(file)
# xunit_executor = ExecutorFactory.get_executor('XUnitStyle')
# xunit_executor.execute(test_sheet)
