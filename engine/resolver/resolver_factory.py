import logging
from engine.resolver.fs_resolver import *
from common.const.vars import FS

LOGGER = logging.getLogger(__name__)


class ResolverFactory:
    '''
    Factory for the executor. As of now only one type of executor is supported.
    In future can be enhanced to support multiple executors. Keeps one _instances
    private attribute, so that it can keep the singleton instances. Everytime the get_executor
    is called it first checks if it has the instance of the specific type or not. If instance is
    present , returns the same from the _instances map or else creates a new and puts into the map.
    '''

    _instances = {}

    @staticmethod
    def get_resolver(type):
        '''
        Factory method to return appropriate resolver based on the input type.

        :param type: string
        :return: Resolver
        '''
        if not type:
            LOGGER.error('ExecutorFactory: type is not provided')
            return

        if type == FS:
            resolver = ResolverFactory._instances.get(type, None)
            if not resolver:
                resolver = FSPathResolver()
                ResolverFactory._instances[type] = resolver
            return resolver
        else:
            LOGGER.warn('ExecutorFactory:get_executor invalid type')
            return None
