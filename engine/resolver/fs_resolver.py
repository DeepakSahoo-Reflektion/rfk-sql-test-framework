from codecs import open
import os
import logging

from engine.resolver.resolver import PathResolver

LOGGER = logging.getLogger(__name__)


class FSPathResolver(PathResolver):
    '''
    PathResolver implementation of the file system.
    '''

    def resolve(self, file_path):
        '''
        Method which will take the file_path as argument and returns the contents.
        The file_path argument should be an absolute location.
        :param file_path: string containing file path location
        :return:
        '''
        try:
            file_string = None
            f = open(file_path, 'r', encoding='utf-8')
            file_string = f.read()
        except Exception as e:
            LOGGER.error('Error while reading the file.. %s', e.args)
            raise e
        finally:
            f.close()
        return file_string
