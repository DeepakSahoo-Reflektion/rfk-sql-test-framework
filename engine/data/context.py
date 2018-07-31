import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class ContextManager(object):

    @staticmethod
    def initialize_default(type = None):
        if not type:
            return
        logger.info('ContextManager:initialize_default with type %s', type)
        if type == 'case':
            return CaseContext().with_default()
        elif type == 'sheet':

            return SheetContext().with_default()
        elif type == 'suite':
            return SuiteContext().with_default()
        else:
            logger.error('Invalid type..')
            raise Exception('Invalid type...')


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

    # def __init__(self):
    #     pass
    #
    # def add_attribute(self, attr_name, attr_value=None):
    #     self.__dict__[attr_name] = attr_value
    #
    # def remove_attribute(self, attr_name):
    #     del self.__dict__[attr_name]
    #
    # def get_attributes(self):
    #     return self.__dict__.items()


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

    # def initialize(self, dict):
    #     self.sql_path = dict.get('sql_path', None)
    #     self.script_path = dict.get('script_path', None)
    #     self.cases_count = dict.get('', None)


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