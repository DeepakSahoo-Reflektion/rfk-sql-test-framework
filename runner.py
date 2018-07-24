from engine.data.suite import TestSuite
from engine.executor.case_executor import *
from engine.parser.custom_json_parser import *

def main():
    ## TODO : scan all the test files recursively in the location
    print('')

    ## TODO: create the test suite for the entire framework
    suite = TestSuite()

    ## TODO : for each test configuration file create the data object or dict
    ## TODO : create the test sheet from the config parser

    sheet = JsonParser().parse()

    ## TODO: now give the test sheet to appropriate executor, so get the appropriate executor from the factory
    executor = ExecutorFactory().get_executor('XUnitStyle')

    ## TODO : give the executor the test sheet to execute
    ## TODO : result will be an instance of TestResult class
    result = executor.execute(sheet)

    ##TODO : add each test sheet to the suite
    ## suite.add_test_sheet(sheet)
    suite.add_result(result)

    ## TODO: end of line





if __name__ == 'main':
    main()
