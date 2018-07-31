import logging
##TODO: parse the query result in Assert_handler
##TODO: create the sql and expected using the script_path in Assert_handler
##TODO: if needed create separate Result class to return the results

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

from engine.data.result import *

class SheetHandler(object):
    '''
    This is a COR pattern implementation of our execution sequence. one execution delegates the process to another
    one instead of doing it all alone.
    '''

    def __init__(self,service):
        logger.info('SheetHandler:init')
        self._service = service
        self._handler = CaseHandler(service)
        self._result = None
        self._meta_args = {}

    def _create_meta_args(self,test_sheet):
        logger.info('SheetHandler:_create_meta_args ENTRY with %s', test_sheet)

        self._meta_args['sheet_name'] =  test_sheet.get('name',None)
        self._meta_args['sql_path'] = test_sheet.get('sql_path',None)
        self._meta_args['script_path'] = test_sheet.get('script_path',None)

        logger.info('SheetHandler:_create_meta_args EXIT with %s', test_sheet)

    def handle_request(self,test_sheet):
        logger.info('SheetHandler:handle_request ENTRY with %s',test_sheet)
        self._create_meta_args(test_sheet)
        self._service.serve(test_sheet.get('before_once',None))

        sheet_name = test_sheet.get('name',None)
        sheet_result = SheetResult(name=sheet_name, status='Success')
        count = 0

        for case in test_sheet.get('tests',None):
            self._service.serve(test_sheet.get('before_each', None))

            case_name = case.get('name',None)
            case_result = self._handler.handle_request(case,self._meta_args)
            ##self._results[case_name] = case_result

            count += 1
            sheet_result.add_case_result(count,case_result)

            if case_result.status == 'Failure':
                sheet_result.update_status('Failure')

            self._service.serve(test_sheet.get('after_each', None))

        self._service.serve(test_sheet.get('after_once', None))
        self._result = sheet_result

        return self._result

class CaseHandler(object):

    def __init__(self,service):
        logger.info('CaseHandler:init')
        self._service = service
        self._handler = AssertHandler(service)
        self._result = None

    def handle_request(self,test_case,meta_args):
        logger.info('CaseHandler:handle_request ENTRY with %s', test_case)
        self._service.serve(test_case.get('before_test', None))

        case_name = test_case.get('name', None)

        self._service.serve(meta_args['script_path'])
        count = 0
        case_result = CaseResult(name=case_name,status='Success')
        for each_assert in test_case.get('asserts', None):

            assert_result = self._handler.handle_request(each_assert,meta_args)
            count += 1

            case_result.add_assert_result(count,assert_result)

            if assert_result.status == 'Failure':
                case_result.update_status('Failure')
            ##self._result['assert-{}'.format(count)]=assert_result


        self._service.serve(test_case.get('after_test', None))
        self._result = case_result
        logger.info('CaseHandler:handle_request with result %s',case_result)
        return self._result


## TODO: to change the sql query replace enricher with a decorator
class AssertHandler(object):

    def __init__(self,service):
        logger.info('AssertHandler:init')
        self._service = service
        self._result = None

    def content_enrich(self,args):
        pass


    def handle_request(self,each_assert,meta_args):
        self._service.serve(each_assert.get('expected', None))
        ##self._service.serve(CommandObject(type='sql',opr='execute_statement',payload=None))

        sql_query = each_assert.get('sql', None)
        query_result = self._service.serve(sql_query)

        logger.info('AssertHandler:handle_request query_result %s', query_result)
        message = each_assert.get('message', None)

        status = 'Failure'
        if len(query_result) != 0 and len(query_result[1]) == 0:
            status='Success'

        self._result = AssertResult(message=message,status=status)
        return self._result