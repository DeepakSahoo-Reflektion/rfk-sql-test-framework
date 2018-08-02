import logging
from engine.resolver.git_resolver import *
from engine.resolver.fs_resolver import *
from engine.resolver.s3_resolver import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

## TODO: improvise the if else condition
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
        if not type:
            logger.error('ExecutorFactory: type is not provided')
            return

        if type == 'git':
            resolver = ResolverFactory._instances.get(type,None)
            if not resolver:
                resolver =  GitPathResolver()
                ResolverFactory._instances[type] = resolver
            return resolver
        elif type == 'fs':
            resolver = ResolverFactory._instances.get(type, None)
            if not resolver:
                resolver = FSPathResolver()
                ResolverFactory._instances[type] = resolver
            return resolver
        elif type == 's3':
            resolver = ResolverFactory._instances.get(type, None)
            if not resolver:
                resolver = S3PathResolver()
                ResolverFactory._instances[type] = resolver
            return resolver

        else:
            logger.warn('ExecutorFactory:get_executor invalid type')
            return None