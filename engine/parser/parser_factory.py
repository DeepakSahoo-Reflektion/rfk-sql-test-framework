import logging

from engine.parser.json_parser import *
from engine.parser.yaml_parser import *


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

class ParserFactory:
    '''
    Factory for the executor. As of now only one type of executor is supported.
    In future can be enhanced to support multiple executors. Keeps one _instances
    private attribute, so that it can keep the singleton instances. Everytime the get_executor
    is called it first checks if it has the instance of the specific type or not. If instance is
    present , returns the same from the _instances map or else creates a new and puts into the map.
    '''

    _instances = {}

    @staticmethod
    def get_parser(type):
        if not type:
            LOGGER.error('ExecutorFactory: type is not provided')
            return

        if type in ('json','.json'):
            parser = ParserFactory._instances.get(type,None)
            if not parser:
                parser =  JsonParser()
                ParserFactory._instances[type] = parser
            return parser
        elif type in ('yaml','.yaml','yml','.yml'):
            parser = ParserFactory._instances.get(type, None)
            if not parser:
                parser = YamlParser()
                ParserFactory._instances[type] = parser
            return parser

        else:
            LOGGER.warn('ExecutorFactory:get_executor invalid type')
            return None