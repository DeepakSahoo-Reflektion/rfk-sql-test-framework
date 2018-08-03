import logging

from engine.executor.executor import Executor
from engine.handler.handler import SheetHandler
from engine.service.service_facade import ServiceFacade

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


class XUnitStyleExecutor(Executor):
    def __init__(self, context):
        super().__init__()
        self._service = ServiceFacade(context)
        self._handler = SheetHandler(self._service)

    def execute(self, sheet):
        '''
        Entry point of the executor. calls the handler for executing the operations.
        This is a delegator which doesn't have messy execution logic. instead delegates
        the request to the handlers for execution.

        :param sheet: as the configuration sheet instance
        :return: SheetResult instance when complete successfully
        '''
        LOGGER.debug('XUnitStyleExecutor:execute ENTRY with %s', sheet)
        result = None
        try:
            result = self._handler.handle_request(sheet)

        except AttributeError as e:
            LOGGER.error('XUnitStyleExecutor:Attribute Error .. %s', e.args)

        except Exception as e:
            LOGGER.error('XUnitStyleExecutor:Some exception raised .. %s', e.args)
        finally:
            LOGGER.info('Closing the connections.......')
            self._service.close()

        LOGGER.info('XUnitStyleExecutor:execute EXIT with result %s', result)
        return result
