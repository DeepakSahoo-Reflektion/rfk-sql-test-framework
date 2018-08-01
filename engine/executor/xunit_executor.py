import logging

from engine.executor.executor import Executor
from engine.service.db_service import DBService
from engine.handler.handler import SheetHandler
from engine.service.service_facade import ServiceFacade

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class XUnitStyleExecutor(Executor):

    def __init__(self,context):
        super().__init__()
        logger.info('XUnitStyleExecutor: Init')
        self._service = ServiceFacade(context)
        self._handler = SheetHandler(self._service)

    def execute(self, sheet):
        '''
        Entry point of the executor. calls the handler for executing the operations.

        :param sheet: as the configuration sheet instance
        :return: SheetResult instance when complete successfully
        '''
        logger.debug('XUnitStyleExecutor:execute ENTRY with %s', sheet)
        try:
             result = self._handler.handle_request(sheet)

        except AttributeError as e:
            logger.error('XUnitStyleExecutor:Attribute Error .. %s', e.args)

        except Exception as e:
            logger.error('XUnitStyleExecutor:Some exception raised .. %s',e.args)
        finally:
            logger.info('Closing the connections.......')
            self._service.close()

        logger.info('XUnitStyleExecutor:execute EXIT with result %s',result)
        return result

