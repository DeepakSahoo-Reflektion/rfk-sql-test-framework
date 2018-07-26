import logging

from engine.executor.executor import Executor
from engine.service.service import DBService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

## TODO : make the attributes_list as a stack and pop the attributes in order till the stack is empty and invoke
class XUnitStyleExecutor(Executor):

    def __init__(self):
        logger.info('XUnitStyleExecutor: Init')
        self.attributes_seq_stack = ['after_once','after_each','tests','before_each','before_once']
        self._service = DBService()
        self._handler = SheetHandler(self._service)

    def execute(self, sheet):
        try:
            self._handler.handle_request(sheet)
        except Exception as e:
            logger.error('Some exception raised .. %s',e.args)
            self._service.close()

class SheetHandler(object):

    def __init__(self,service):
        self._service = service
        self._handler = CaseHandler(service)

    def handle_request(self,test_sheet):
        self._service.serve(test_sheet.__getattribute__('before_once'))

        for case in test_sheet.__getattribute__('tests'):
            self._service.serve(test_sheet.__getattribute__('before_each'))

            case_result = self._handler.handle_request(case)

            self._service.serve(test_sheet.__getattribute__('after_each'))

        self._service.serve(test_sheet.__getattribute__('after_once'))

class CaseHandler(object):

    def __init__(self,service):
        self._service = service
        self._handler = AssertHandler(service)

    def handle_request(self,test_case):
        self._service.serve(test_case.__getattribute__('before_test'))

        for each_assert in test_case.__getattribute__('asserts'):
            assert_result = self._handler.handle_request(each_assert)

        self._service.serve(test_case.__getattribute__('after_test'))


class AssertHandler(object):

    def handle_request(self,each_assert):
        logger.info('XUnitStyleExecutor:execute_assert ENTRY with args %s', each_assert)
        sql = each_assert.__getattribute__('sql')
        ret_value = self.run_script(sql) if is_sql_script(sql) else self.run_statments(sql)

        expected = each_assert.get('expected', None)
        ret_value = self.run_script(sql) if is_sql_script(sql) else self.run_statments(sql)
