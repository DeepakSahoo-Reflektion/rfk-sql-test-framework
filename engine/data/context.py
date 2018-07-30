import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class SuiteContext(object):

    def __init__(self):
        pass

    def add_attribute(self,attr_name,attr_value = None):
        self.__dict__[attr_name] = attr_value

    def remove_attribute(self,attr_name):
        del self.__dict__[attr_name]

    def get_attributes(self):
        return self.__dict__.items()