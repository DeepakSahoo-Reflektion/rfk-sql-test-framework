import logging

from common.const.vars import *
from common.util.sql_util import *
from engine.data.result import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class SheetHandler(object):
    '''
    This is a COR pattern implementation of our execution sequence. one execution delegates the process to another
    one instead of doing it all alone.
    '''

    def __init__(self, service):
        '''
        Initializes the paramters for the SheetHandler.

        :param service: the type of Service implementation class.
        '''
        self._service = service
        self._handler = CaseHandler(service)
        self._result = None
        self._meta_args = {}

    def _create_meta_args(self, test_sheet):
        logger.debug('SheetHandler:_create_meta_args ENTRY with %s', test_sheet)

        self._meta_args[NAME] = test_sheet.get(NAME, None)
        self._meta_args[SQL_PATH] = test_sheet.get(SQL_PATH, None)
        self._meta_args[SCRIPT_PATH] = test_sheet.get(SCRIPT_PATH, None)

        logger.info('SheetHandler:_create_meta_args EXIT with %s', test_sheet)

    def handle_request(self, test_sheet):
        logger.debug('SheetHandler:handle_request ENTRY with %s', test_sheet)
        self._create_meta_args(test_sheet)
        self._service.serve(test_sheet.get(BEFORE_ONCE, None))

        sheet_name = test_sheet.get(NAME, None)
        sheet_result = SheetResult(name=sheet_name, status=STATUS_SUCCESS)
        count = 0

        for case in test_sheet.get(TESTS, None):
            self._service.serve(test_sheet.get(BEFORE_EACH, None))

            case_name = case.get(NAME, None)
            case_result = self._handler.handle_request(case, self._meta_args)

            count += 1
            sheet_result.add_case_result(count, case_result)

            if case_result.status == STATUS_FAILURE:
                sheet_result.update_status(STATUS_FAILURE)

            self._service.serve(test_sheet.get(AFTER_EACH, None))

        self._service.serve(test_sheet.get(AFTER_ONCE, None))
        self._result = sheet_result
        logger.info('SheetHandler:handle_request EXIT with %s', self._result)
        return self._result


class CaseHandler(object):
    '''
    COR implementation where it handles only the operations related to the test cases.
    Delegates the assert operations to the AssertHandler
    '''

    def __init__(self, service):
        self._service = service
        self._handler = AssertHandler(service)
        self._result = None

    def handle_request(self, test_case, meta_args):
        logger.debug('CaseHandler:handle_request ENTRY with %s', test_case)
        self._service.serve(test_case.get(BEFORE_TEST, None))

        case_name = test_case.get(NAME, None)

        self._service.serve(meta_args[SCRIPT_PATH])
        count = 0
        case_result = CaseResult(name=case_name, status=STATUS_SUCCESS)
        for each_assert in test_case.get(ASSERTS, None):

            assert_result = self._handler.handle_request(each_assert, meta_args)
            count += 1

            case_result.add_assert_result(count, assert_result)

            if assert_result.status == STATUS_FAILURE:
                case_result.update_status(STATUS_FAILURE)

        self._service.serve(test_case.get(AFTER_TEST, None))
        self._result = case_result
        logger.info('CaseHandler:handle_request with result %s', case_result)
        return self._result


## TODO: to change the sql query replace enricher with a decorator
class AssertHandler(object):
    '''
    Handles the execution of the sql script and statements inside the asserts block inside the configuration.
    '''

    def __init__(self, service):
        self._service = service
        self._result = None

    def content_enrich(self, args):
        pass

    def handle_request(self, each_assert, meta_args):
        self._service.serve(each_assert.get(EXPECTED, None))

        sql_query = each_assert.get(SQL, None)
        enriched_sql_query = enrich_sql(sql_query)
        query_result = self._service.serve(enriched_sql_query)

        message = each_assert.get(MESSAGE, None)

        status = STATUS_FAILURE
        if len(query_result) != 0 and len(query_result[1]) == 0:
            status = STATUS_SUCCESS

        self._result = AssertResult(message=message, status=status)
        logger.info('AssertHandler:handle_request EXIT with %s', self._result)
        return self._result
