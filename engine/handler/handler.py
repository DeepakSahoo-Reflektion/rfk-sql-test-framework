from common.const.vars import *
from common.util.sql_util import *
from engine.data.result import *
from engine.data.context import ContextManager
from engine.service.service_facade import ServiceFacade

LOGGER = logging.getLogger(__name__)


class SheetHandler(object):
    '''
    This is a COR pattern implementation of our execution sequence. one execution delegates the process to another
    one instead of doing it all alone.
    '''

    def __init__(self, context):
        '''
        Initializes the paramters for the SheetHandler. We have used the DTO pattern to communicate between different layers.
        Here the context objects act as Data transfer objects.

        :param service: the type of Context, here SheetContext
        '''
        self._handler = CaseHandler(context)
        self._service = context.get_instance(SERVICE_INSTANCE)

    def handle_request(self, context):
        sheet_data = context.get_data()
        LOGGER.info('SheetHandler:handle_request ENTRY with %s', sheet_data)
        self._service.serve(sheet_data.get(BEFORE_ONCE, None))
        result = SheetResult(name=sheet_data.get(NAME, None), status=STATUS_SUCCESS)

        count = 0
        for case in sheet_data.get(TESTS, None):
            self._service.serve(sheet_data.get(BEFORE_EACH, None))

            case_context = ContextManager.initialize_default(CASE).update_data(case).update_params(
                {SCRIPT_PATH: sheet_data.get(SCRIPT_PATH, None)})
            context.update_contexts({'Context-{}'.format(count): self._handler.handle_request(case_context)})
            count += 1

            LOGGER.info('will run after each over..')
            self._service.serve(sheet_data.get(AFTER_EACH, None))

        self._service.serve(sheet_data.get(AFTER_ONCE, None))
        ## TODO:result
        context.update_result(result)
        LOGGER.info('SheetHandler:handle_request EXIT with %s', context)
        return context


class CaseHandler(object):
    '''
    COR implementation where it handles only the operations related to the test cases.
    Delegates the assert operations to the AssertHandler
    '''

    def __init__(self, context):
        self._handler = AssertHandler(context)
        self._service = context.get_instance(SERVICE_INSTANCE)

    def handle_request(self, context):
        case_data = context.get_data()
        LOGGER.info('CaseHandler:handle_request ENTRY with %s', case_data)

        self._service.serve(case_data.get(BEFORE_TEST, None))
        self._service.serve(context.get_param(SCRIPT_PATH))
        LOGGER.info('CaseHandler:handle_request ENTRY with %s', case_data)
        count = 0
        for each_assert in case_data.get(ASSERTS, None):
            assert_context = ContextManager.initialize_default(ASSERT).update_data(each_assert)
            context.update_contexts({'Context-{}'.format(count): self._handler.handle_request(assert_context)})
            count += 1

            # if case_result.status == STATUS_FAILURE:
            #     sheet_result.update_status(STATUS_FAILURE)

        self._service.serve(case_data.get(AFTER_TEST, None))

        ## TODO: status
        result = CaseResult(context.get_param(NAME), status=STATUS_SUCCESS)
        context.update_result(result)
        return context


class AssertHandler(object):
    '''
    Handles the execution of the sql script and statements inside the asserts block inside the configuration.
    '''

    def __init__(self, context):
        self._service = context.get_instance(SERVICE_INSTANCE)

    def handle_request(self, context):
        assert_data = context.get_data()
        LOGGER.info('AssertHandler with assert_data %s', assert_data)

        self._service.serve(assert_data.get(EXPECTED, None))

        sql_query = assert_data.get(SQL, None)
        LOGGER.info('AssertHandler with sql_query %s', sql_query)
        enriched_sql_query = enrich_sql(sql_query)
        LOGGER.info('AssertHandler with enriched_sql_query %s', enriched_sql_query)
        query_result = self._service.serve(enriched_sql_query)

        message = assert_data.get(MESSAGE, None)
        LOGGER.info('AssertHandler with message %s', message)

        status = STATUS_FAILURE
        if len(query_result) != 0 and len(query_result[1]) == 0:
            status = STATUS_SUCCESS

        result = AssertResult(message=message, status=status)

        LOGGER.info('AssertHandler:handle_request EXIT with %s', result)
        context.update_result(result)
        return context
