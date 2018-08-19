from common.const.vars import *
from common.util.sql_util import *
from common.util.common_util import *
from engine.data.result import *
from engine.data.context import ContextManager
from engine.service.service_facade import ServiceFacade
from engine.generator.query_generator import QueryGenerator
from engine.generator.data_generator import DataGenerator
from engine.comparator.result_comparator import ResultComparator
from engine.handler.assert_handler import AssertHandler

LOGGER = logging.getLogger(__name__)

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

        count = 1
        failed_asserts = skipped_asserts = []

        for each_assert in case_data.get(ASSERTS, None):

            is_skip = each_assert.get(SKIP, None)
            LOGGER.info('is_skip %s', is_skip)

            if is_skip is None or is_skip != TRUE:
                assert_context = ContextManager.initialize_default(ASSERT).update_data(each_assert)
                LOGGER.info("-------------------- ASSERTIONS:{} START-----------------".format(count))
                LOGGER.info("\n")
                updated_assert_context = self._handler.handle_request(assert_context)
                LOGGER.info("\n")
                LOGGER.info("-------------------- ASSERTIONS:{} END-----------------".format(count))

                name = 'Context-{}'.format(count)

                if updated_assert_context.result.get_status() == STATUS_FAILURE:
                    failed_asserts.append(name)
                if updated_assert_context.result.get_status() == STATUS_SKIPPED:
                    skipped_asserts.append(name)
                context.update_contexts({name: updated_assert_context})
            count += 1

        self._service.serve(case_data.get(AFTER_TEST, None))

        result = CaseResult(STATUS_SUCCESS if len(failed_asserts) == 0 else STATUS_FAILURE, failed_asserts,skipped_asserts)
        context.update_result(result)
        return context