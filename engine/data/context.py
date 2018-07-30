import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class SheetContext(object):

    def __init__(self):
        self.sheet = None
        self.dict = {}
        self.cases_executed = 0

    def initialize(self,dict):
        self.sql_path = dict.get('sql_path',None)
        self.script_path = dict.get('script_path', None)
        self.cases_count = dict.get('', None)


class SuiteContext(object):

    def __init__(self):
        pass

    def add_attribute(self,attr_name,attr_value = None):
        self.__dict__[attr_name] = attr_value

    def remove_attribute(self,attr_name):
        del self.__dict__[attr_name]

    def get_attributes(self):
        return self.__dict__.items()