##TODO: parse the query result in Assert_handler
##TODO: create the sql and expected using the script_path in Assert_handler
##TODO: if needed create separate Result class to return the results
class SheetHandler(object):
    '''
    This is a COR pattern implementation of our execution sequence. one execution delegates the process to another
    one instead of doing it all alone.
    '''

    def __init__(self,service):
        self._service = service
        self._handler = CaseHandler(service)
        self._results = {}
        self._meta_args = {}

    def _create_meta_args(self,test_sheet):
        sheet_name = test_sheet.__getattribute__('name')
        sql_path = test_sheet.__getattribute__('sql_path')
        script_path = test_sheet.__getattribute__('script_path')
        self._meta_args['sheet_name'] = sheet_name
        self._meta_args['sql_path'] = sql_path
        self._meta_args['script_path'] = script_path

    def handle_request(self,test_sheet):
        self._create_meta_args(test_sheet)
        self._service.serve(test_sheet.__getattribute__('before_once'))

        for case in test_sheet.__getattribute__('tests'):
            self._service.serve(test_sheet.__getattribute__('before_each'))

            case_name = case.__getattribute__('name')
            case_result = self._handler.handle_request(case,self._meta_args)
            self._results[case_name] = case_result

            self._service.serve(test_sheet.__getattribute__('after_each'))

        self._service.serve(test_sheet.__getattribute__('after_once'))

        return self._results

class CaseHandler(object):

    def __init__(self,service):
        self._service = service
        self._handler = AssertHandler(service)
        self._result = {}

    def handle_request(self,test_case,sql_script,meta_args):
        self._service.serve(test_case.__getattribute__('before_test'))

        self._service.serve(meta_args['script_path'])
        count = 0
        for each_assert in test_case.__getattribute__('asserts'):

            assert_result = self._handler.handle_request(each_assert,meta_args)
            self._result['assert-{}'.format(count)]=assert_result
            count += 1

        self._service.serve(test_case.__getattribute__('after_test'))
        return self._result


class AssertHandler(object):

    def __init__(self,service):
        self._service = service
        self._result = None

    def handle_request(self,each_assert,meta_args):
        self._service.serve(each_assert.__getattribute__('sql'))

        query_result = self._service.serve(each_assert.__getattribute__('expected'))
        self._result = query_result
        return self._result
