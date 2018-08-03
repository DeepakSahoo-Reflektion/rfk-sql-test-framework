import logging

from common.const.vars import XUNIT
from engine.service.service import *
from engine.executor.xunit_executor import XUnitStyleExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class ExecutorFactory:
    '''
    Factory for the executor. As of now only one type of executor is supported.
    In future can be enhanced to support multiple executors. Keeps one _instances
    private attribute, so that it can keep the singleton instances. Everytime the get_executor
    is called it first checks if it has the instance of the specific type or not. If instance is
    present , returns the same from the _instances map or else creates a new and puts into the map.
    '''

    _instances = {}

    @staticmethod
    def get_executor(type, context):

        if not type:
            logger.error('ExecutorFactory: type is not provided')
            return

        if type == XUNIT:
            executor = ExecutorFactory._instances.get(type, None)
            if not executor:
                executor = XUnitStyleExecutor(context)
            ExecutorFactory._instances[type] = executor
            return executor

        else:
            logger.error('ExecutorFactory:get_executor invalid type')
            raise Exception('Invalid Executor Type...')
