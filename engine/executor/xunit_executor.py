import logging

from engine.executor.executor import Executor
from engine.handler.handler import SheetHandler
from engine.service.service_facade import ServiceFacade
from common.const.vars import SERVICE_INSTANCE

LOGGER = logging.getLogger(__name__)


class XUnitStyleExecutor(Executor):
    '''
    xunit style of implementation of Executor interface. Xunit style follows a sequence of execution.
        before_once : will be evaluated only once for the entire configuration file.
        before_each : will be evaluated prior to each test execution.
        before_test : will be evaluated prior to specific test execution.
        after_test  : will be evaluated after each specific test execution.
        after_each  : will be evaluated after  each test execution.
        after_once  : will be evaluated only once after all execution for the entire configuration file.
    '''
    def __init__(self,context):
        super().__init__()
        self._service = ServiceFacade(context)
        context.update_instances({SERVICE_INSTANCE: self._service})
        self._handler = SheetHandler(context)

    def execute(self,context):
        '''
        Entry point of the executor. calls the handler for executing the operations.
        This is a delegator which doesn't have messy execution logic. instead delegates
        the request to the handlers for execution.

        :param sheet: as the configuration sheet instance
        :return: SheetResult instance when complete successfully
        '''
        result = None
        try:
            result = self._handler.handle_request(context)

        except AttributeError as e:
            LOGGER.error('XUnitStyleExecutor:Attribute Error .. %s', e.args)

        except Exception as e:
            LOGGER.error('XUnitStyleExecutor:Some exception raised .. %s', e.args)
            raise e
        finally:
            LOGGER.info('Closing the connections.......')
            self._service.close()

        LOGGER.info('XUnitStyleExecutor:execute EXIT with result %s', result)
        return result
