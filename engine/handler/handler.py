
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