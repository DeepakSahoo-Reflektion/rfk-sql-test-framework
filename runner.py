# from engine.data.suite import TestSuite
from engine.executor.executor import *
from engine.parser.json_parser import *
from engine.resolver.fs_resolver import FileLocPathResolver

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


def invoke_single(test_sheet_loc= None):
    if not test_sheet_loc:
        logger.error('Runner: Error in the file location')
        raise ValueError('Test-Sheet location is not provided for single execution')

    logger.info('Runner: Creating the fileLocPathResolver')
    file = FileLocPathResolver().resolve(test_sheet_loc)

    logger.info('Runner: Creating the test-sheet')
    ## TODO : create the Test-Sheet instance by calling the parser
    test_sheet = JsonParser().parse(file)

    logger.info('Runner: Creating the executor')
    executor = ExecutorFactory().get_executor('XUnitStyle')
    logger.info('Runner : executor created')
    executor.execute(test_sheet)


# if __name__ == '__main__':
#     print('starting..')
#     invoke_single('/Users/deepak/PycharmProjects/rfk-sql-test-framework/test_config_file.json')

print(__name__)
invoke_single('/Users/deepak/PycharmProjects/rfk-sql-test-framework/sample_config_file.json')
