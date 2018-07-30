# from engine.data.suite import TestSuite
from engine.executor.executor import *
from engine.executor.executor_factory import ExecutorFactory
from engine.parser.json_parser import *
from engine.resolver.fs_resolver import FSPathResolver
from engine.data.context import SuiteContext

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# def main():
#     ## TODO : scan all the test files recursively in the location
#     print('')
#
#     ## TODO : get the connection object here from the snowflake_connection and pass to the suite
#     ##conn =
#
#     ## TODO: create the test suite for the entire framework
#     suite = TestSuite()
#
#     ## TODO : for each test configuration file create the data object or dict
#     ## TODO : create the test sheet from the db parser
#
#     sheet = JsonParser().parse()
#
#     ## TODO: now give the test sheet to appropriate executor, so get the appropriate executor from the factory
#     executor = ExecutorFactory().get_executor('XUnitStyle')
#
#     ## TODO : give the executor the test sheet to execute
#     ## TODO : result will be an instance of TestResult class
#     sheet_result = executor.execute(sheet)
#
#     ##TODO : add each test sheet to the suite
#     ## suite.add_test_sheet(sheet)
#     suite.add_result(sheet_result)
#
#     ## TODO: end of line


def invoke_single(context,test_sheet_loc= None):
    if not test_sheet_loc:
        logger.error('Runner: Error in the file location')
        raise ValueError('Test-Sheet location is not provided for single execution')

    logger.info('Runner: Creating the fileLocPathResolver')
    file = FSPathResolver().resolve(test_sheet_loc)

    logger.info('Runner: Creating the test-sheet')
    ## TODO : create the Test-Sheet instance by calling the parser
    test_sheet = JsonParser().parse(file)

    ##context.add_attribute(test_sheet_loc,test_sheet)

    logger.info('Runner: Creating the executor')
    executor = ExecutorFactory().get_executor('XUnitStyle')
    logger.info('Runner : executor created')
    executor.execute(test_sheet)


# if __name__ == '__main__':
#     print('starting..')
#     invoke_single('/Users/deepak/PycharmProjects/rfk-sql-test-framework/test_config_file.json')

print(__name__)

if __name__ == '__main__':
    context = SuiteContext()
    invoke_single(context,'/Users/deepak/PycharmProjects/rfk-sql-test-framework/running_config_be_step1_inventory.json')

