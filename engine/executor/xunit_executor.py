import logging

from engine.executor.executor import Executor
from engine.service.service import DBService
from engine.handler.handler import SheetHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

## TODO : make the attributes_list as a stack and pop the attributes in order till the stack is empty and invoke
class XUnitStyleExecutor(Executor):

    def __init__(self):
        logger.info('XUnitStyleExecutor: Init')
        self.attributes_seq_stack = ['after_once','after_each','tests','before_each','before_once']
        self._service = DBService()
        self._handler = SheetHandler(self._service)

    def execute(self, sheet):
        try:
            self._handler.handle_request(sheet)
        except Exception as e:
            logger.error('Some exception raised .. %s',e.args)
            self._service.close()
