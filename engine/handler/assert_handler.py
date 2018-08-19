from common.const.vars import *
from common.util.sql_util import *
from common.util.common_util import *
from engine.data.result import *
from engine.data.context import ContextManager
from engine.service.service_facade import ServiceFacade
from engine.generator.query_generator import QueryGenerator
from engine.generator.data_generator import DataGenerator
from engine.comparator.result_comparator import ResultComparator

LOGGER = logging.getLogger(__name__)

class AssertHandler(object):
    '''
    Handles the execution of the sql script and statements inside the asserts block inside the configuration.
    '''

    def __init__(self, context):
        self._service = context.get_instance(SERVICE_INSTANCE)
        self._query_generator = QueryGenerator()
        self._data_generator = DataGenerator()
        self._result_comparator = ResultComparator()

    def handle_request(self, context):
        '''
        ## steps:-
        ##	1. extract the predicate types:- none, value, list etc from the sql.
        ##	2. If it is not value or list type then execute the expected or else keep them for comparison.
        ## 	3. calls the sql_generator to generate the enriched_sql or trimmed sql for execution.
        ##	4. execute the executable sql query.
        ##	5.
        :param context:
        :return:
        '''
        try:

            assert_data = context.get_data()
            LOGGER.debug('AssertHandler with assert_data %s', assert_data)

            expected = assert_data.get(EXPECTED, None)
            sql_query = assert_data.get(SQL, None)
            condition = assert_data.get(CONDITION, None)
            predicate_type, _ = extract_query_and_predicate_from(sql_query)

            if predicate_type is None:
                self._service.serve(expected)
            else:
                enriched_expected_data = self._data_generator.generate(expected)

            executable_sql = self._query_generator.generate(sql_query)
            query_result = self._service.serve(executable_sql)
            LOGGER.info('AssertHandler with query execution result %s', query_result)

            status = STATUS_FAILURE
            if predicate_type is None:
                if len(query_result) != 0 and len(query_result[1]) == 0:
                    status = STATUS_SUCCESS

            else:
                result_data = query_result[1] if query_result is not None and query_result[1] is not None else None
                if self._result_comparator.compare(result_data, enriched_expected_data, condition, predicate_type):
                    status = STATUS_SUCCESS

            message = assert_data.get(MESSAGE, None)
            LOGGER.info('AssertHandler with message %s', message)

            result = AssertResult(message=message, status=status)
        except Exception as e:
            LOGGER.error('AssertHandler:handle_request Exception..',e.args)
            result = AssertResult(message='Assertion skipped due to Exception', status=STATUS_SKIPPED)

        LOGGER.info('AssertHandler:handle_request EXIT with %s', result)
        context.update_result(result)
        return context
