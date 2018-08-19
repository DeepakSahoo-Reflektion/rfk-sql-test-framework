from common.const.vars import *
from common.util.sql_util import *
from common.util.common_util import *
from engine.data.result import *
from engine.data.context import ContextManager
from engine.service.service_facade import ServiceFacade
from engine.generator.query_generator import QueryGenerator
from engine.generator.data_generator import DataGenerator
from engine.comparator.result_comparator import ResultComparator
from engine.handler.case_handler import CaseHandler

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

        count = 1
        failed_cases = []

        for case in sheet_data.get(TESTS, None):
            LOGGER.info('case_data %s',case)
            is_skip = case.get(SKIP, None)
            LOGGER.info('is_skip %s',is_skip)

            if is_skip is None or is_skip != TRUE:

                self._service.serve(sheet_data.get(BEFORE_EACH, None))

                case_context = ContextManager.initialize_default(CASE).update_data(case).update_params(
                    {SCRIPT_PATH: sheet_data.get(SCRIPT_PATH, None)})
                name = 'Context-{}'.format(count)
                LOGGER.info("{} TEST CASE {} START- {}".format("-" * 100, count, "-" * 100))
                LOGGER.info("-" * 10)
                LOGGER.info("\n")
                updated_case_context = self._handler.handle_request(case_context)
                LOGGER.info("\n")
                LOGGER.info("-" * 10)
                LOGGER.info("{} TEST CASE {} END- {}".format("-" * 100, count, "-" * 100))
                LOGGER.info(
                    "------------------------------------------- TEST CASE END- {}-------------------------------------------".format(
                        count))

                if updated_case_context.result.get_status() == STATUS_FAILURE:
                    failed_cases.append(name)

                context.update_contexts({name: updated_case_context})


                self._service.serve(sheet_data.get(AFTER_EACH, None))
            count += 1

        self._service.serve(sheet_data.get(AFTER_ONCE, None))
        result = SheetResult(STATUS_SUCCESS if len(failed_cases) == 0 else STATUS_FAILURE, failed_cases)
        context.update_result(result)
        LOGGER.info('SheetHandler:handle_request EXIT with %s', context)
        return context