import abc
import logging
import argparse

from common.util.file_util import *
from common.const.vars import *

from engine.executor.executor_factory import ExecutorFactory
from engine.resolver.resolver_factory import *
from engine.parser.parser_factory import ParserFactory
from engine.data.context import *
from engine.runner.execution_strategy import *

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


class ExecutionStrategy(metaclass=abc.ABCMeta):
    """
    Declare an interface common to all supported algorithms. Context
    uses this interface to call the algorithm defined by a
    ConcreteStrategy.
    """

    @abc.abstractmethod
    def execute(self):
        pass

    def execute_sheet(self, sheet_context):
        sheet_context.update_params({FILE_EXT: get_file_ext(sheet_context.get_param(FILE_PATH_LOC))})

        file = ResolverFactory.get_resolver(sheet_context).resolve(
            sheet_context.get_param(FILE_PATH_LOC))

        sheet = ParserFactory.get_parser(sheet_context).parse(file)
        sheet_context.update_data(sheet)

        result = ExecutorFactory.get_executor(sheet_context).execute(sheet_context)

        return sheet_context


class ExecuteOneStrategy(ExecutionStrategy):
    """
    Implement the algorithm using the Strategy interface.
    """

    def __init__(self, context):
        self._context = context

    def execute(self):
        sheet_context = ContextManager.initialize_default(SHEET).update_params(
            self._context.get_params([LOC_TYPE, EXEC_TYPE, FILE_PATH_LOC]))
        LOGGER.info('ExecutionOneStrategy with %s',sheet_context)
        self._context.update_contexts({'Context-1': self.execute_sheet(sheet_context)})
        return self._context


class ExecuteAllStrategy(ExecutionStrategy):
    """
    Implement the algorithm using the Strategy interface.
    """

    def __init__(self, context):
        self._context = context

    def execute(self):
        for root, dirs, files in os.walk(self._context.get_params(FILE_PATH_LOC)):
            if files:
                count = 1
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.startswith('test_'):
                        sheet_context = ContextManager.initialize_default(SHEET).update_params(
                            self._context.get_params([LOC_TYPE, EXEC_TYPE])).update_params({FILE_PATH_LOC: file_path})

                        self._context.update_contexts({'Context-{}'.format(count): self.execute_sheet(sheet_context)})
                        count += 1
        return self._context


class ExecutionContext:
    def __init__(self, strategy):
        self._strategy = strategy

    def execute(self):
        self._strategy.execute()
