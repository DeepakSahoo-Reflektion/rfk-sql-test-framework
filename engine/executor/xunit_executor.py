import logging

from engine.executor.executor import Executor
from engine.service.service import DBService
from engine.handler.handler import SheetHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

## TODO : make the attributes_list as a stack and pop the attributes in order till the stack is empty and invoke
class XUnitStyleExecutor(Executor):

    def __init__(self):
        super().__init__()
        logger.info('XUnitStyleExecutor: Init')
        self.attributes_seq_stack = ['after_once','after_each','tests','before_each','before_once']
        self._service = DBService()
        self._handler = SheetHandler(self._service)
        ##self._handler = SheetHandler(None)

    def execute(self, sheet):
        logger.info('XUnitStyleExecutor:execute ENTRY with %s', sheet)
        try:
            self._handler.handle_request(sheet)
        except AttributeError as e:
            logger.error('XUnitStyleExecutor:Attribute Error .. %s', e.args)
            self._service.close()
        except Exception as e:
            logger.error('XUnitStyleExecutor:Some exception raised .. %s',e.args)
            self._service.close()
