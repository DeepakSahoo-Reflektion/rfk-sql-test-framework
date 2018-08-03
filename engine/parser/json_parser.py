import json
import logging
from engine.parser.parser import ConfigParser

LOGGER = logging.getLogger(__name__)


class JsonParser(ConfigParser):
    '''
    Json implementation of the ConfigurationParser class
    '''

    def parse(self, file, type=None):
        '''
        parses the json file into dict.
        :param file:
        :param type:
        :return:
        '''
        try:
            if not type:
                return json.loads(file)

            return json.loads(file, object_hook=type)
        except Exception as e:
            LOGGER.error('Failed to parse the JSON file %s', e.args)
            raise e
