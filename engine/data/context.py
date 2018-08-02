import logging

from common.const.vars import CASE,SHEET,SUITE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

##TODO: use the context variables properly in the executor
class ContextManager(object):
    """
    This class is responsible to manage and create different kinds of contexts.
    """

    @staticmethod
    def initialize_default(type = None):
        if not type:
            return

        if type == CASE:
            return CaseContext().with_default()
        elif type == SHEET:
            return SheetContext().with_default()
        elif type == SUITE:
            return SuiteContext().with_default()
        else:
            logger.error('ContextManager:failed to create context,Invalid type..')
            raise Exception('Invalid context type')


class SuiteContext(object):

    def with_default(self):
        self.suit_data = None
        self.kv = {}
        self.total_sheets = 0
        self.sheets_executed = 0
        self.sheets_pending = 0
        self.sheets_succeeded = 0
        self.sheets_failed = 0
        self.status = None
        return self

    def update_params(self,dict):
        self.kv = dict
        logger.info('SuiteContext:update_params with data %s',self.kv)
        return self

class SheetContext(object):

    def with_default(self):
        self.sheet_data = None
        self.kv = {}
        self.total_cases = 0
        self.cases_executed = 0
        self.cases_pending = 0
        self.cases_succeeded = 0
        self.cases_failed = 0
        self.skip_sheet = False
        self.status = None
        self.results = None
        return self

    def update_params(self,dict):
        self.kv = dict
        logger.info('SheetContext:update_params with data %s',self.kv)
        return self

class CaseContext(object):

    def with_default(self):
        self.case_data = None
        self.kv = {}
        self.total_asserts = 0
        self.cases_executed = 0
        self.cases_pending = 0
        self.cases_succeeded = 0
        self.cases_failed = 0
        self.skip_case = False
        self.status = None
        return self