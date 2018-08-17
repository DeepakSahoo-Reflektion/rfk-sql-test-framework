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
        '''
        Basically what we are doing here is:-
            * Accepts sheet_context as part of the argument to the method.
            * Because sheet_context has so many attributes, so extracts the 'data' value.
            * Extract the 'BEFORE_ONCE' attribute and execute.
            * For each case_data inside 'tests' attribute
            *   Extract 'BEFORE_EACH' and execute
            *   Create a case_context object and call the CaseHandler's handle method.
            *   Get the updated_case_context object.
            *   Extract 'AFTER_EACH' attribute and execute.
            * Extract 'AFTER_ONCE' attribute and execute.
            * Prepare the final sheet_result object and add it to the sheet_context
            * returns the final updated sheet_context
        :param context:
        :return:
        '''
        sheet_data = context.get_data()
        LOGGER.debug('SheetHandler:handle_request ENTRY with %s', sheet_data)
        self._service.serve(sheet_data.get(BEFORE_ONCE, None))

        count = 0
        failed_cases = []

        for case in sheet_data.get(TESTS, None):
            self._service.serve(sheet_data.get(BEFORE_EACH, None))

            case_context = ContextManager.initialize_default(CASE).update_data(case).update_params(
                {SCRIPT_PATH: sheet_data.get(SCRIPT_PATH, None)})
            name = 'Context-{}'.format(count)
            LOGGER.info("{} TEST CASE {} START- {}".format("-"*100,count,"-"*100))
            LOGGER.info("-"*10)
            LOGGER.info("\n")
            updated_case_context = self._handler.handle_request(case_context)
            LOGGER.info("\n")
            LOGGER.info("-" * 10)
            LOGGER.info("{} TEST CASE {} END- {}".format("-" * 100, count, "-" * 100))
            LOGGER.info("------------------------------------------- TEST CASE END- {}-------------------------------------------".format(count))


            if updated_case_context.result.get_status() == STATUS_FAILURE:
                failed_cases.append(name)

            context.update_contexts({name: updated_case_context})
            count += 1

            self._service.serve(sheet_data.get(AFTER_EACH, None))

        self._service.serve(sheet_data.get(AFTER_ONCE, None))
        result = SheetResult(STATUS_SUCCESS if len(failed_cases) == 0 else STATUS_FAILURE, failed_cases)
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
        '''
        Basically what we are doing here is:-
            * Accepts case_context as part of the argument to the method.
            * Because case_context has so many attributes, so extracts the 'data' from the case_context.
            * Extract the 'BEFORE_TEST' attribute and execute.
            * Extract 'SCRIPT_PATH' attribute and execute.
            * Extract the assert_data from the case_data
            *   For each assert data create a assert_context.
            *   call the AssertHandler's handle method passing the assert_context.
            *   Get the updated assert_context as part of the return value.
            *   Add each updated_assert_context to the case_context's contexts map.
            * Extract the 'AFTER_TEST' attribute from the case_context and execute.
            * Prepare the final case_result object and add it to the case_context
            * returns the case_context
        :param context:
        :return:
        '''
        case_data = context.get_data()
        LOGGER.debug('CaseHandler:handle_request ENTRY with %s', case_data)

        self._service.serve(case_data.get(BEFORE_TEST, None))
        self._service.serve(context.get_param(SCRIPT_PATH))
        LOGGER.debug('CaseHandler:handle_request ENTRY with %s', case_data)

        count = 0
        failed_asserts = []

        for each_assert in case_data.get(ASSERTS, None):
            assert_context = ContextManager.initialize_default(ASSERT).update_data(each_assert)
            LOGGER.info("-------------------- ASSERTIONS:{} START-----------------".format(count))
            LOGGER.info("\n")
            updated_assert_context = self._handler.handle_request(assert_context)
            LOGGER.info("\n")
            LOGGER.info("-------------------- ASSERTIONS:{} END-----------------".format(count))

            name = 'Context-{}'.format(count)

            if updated_assert_context.result.get_status() == STATUS_FAILURE:
                failed_asserts.append(name)
            context.update_contexts({name: updated_assert_context})
            count += 1

        self._service.serve(case_data.get(AFTER_TEST, None))

        result = CaseResult(STATUS_SUCCESS if len(failed_asserts) == 0 else STATUS_FAILURE, failed_asserts)
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
        LOGGER.debug('AssertHandler with assert_data %s', assert_data)

        self._service.serve(assert_data.get(EXPECTED, None))

        sql_query = assert_data.get(SQL, None)
        LOGGER.info('AssertHandler with sql_query %s', sql_query)
        enriched_sql_query = enrich_sql(sql_query)
        LOGGER.info('AssertHandler with enriched_sql_query %s', enriched_sql_query)
        query_result = self._service.serve(enriched_sql_query)
        LOGGER.info('AssertHandler with query execution result %s', query_result)

        message = assert_data.get(MESSAGE, None)
        LOGGER.info('AssertHandler with message %s', message)

        status = STATUS_FAILURE
        if len(query_result) != 0 and len(query_result[1]) == 0:
            status = STATUS_SUCCESS

        result = AssertResult(message=message, status=status)

        LOGGER.info('AssertHandler:handle_request EXIT with %s', result)
        context.update_result(result)
        return context
