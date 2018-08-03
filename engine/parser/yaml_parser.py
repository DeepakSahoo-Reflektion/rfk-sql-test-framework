import yaml
import os
import logging
from engine.parser.parser import ConfigParser

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


class YamlParser(ConfigParser):
    '''
    Yaml implementation of the ConfigParser
    '''

    def parse(self, file, type=None):
        '''
        Basically parses a yaml file into a dict.
        :param file:
        :param type:
        :return:
        '''
        try:
            return yaml.safe_load(file)
        except Exception as e:
            LOGGER.error('Failed to parse the YAML file %s', e.args)
            raise e
