# from engine.data.suite import TestSuite
from engine.executor.executor import *
from engine.executor.executor_factory import ExecutorFactory
from engine.parser.json_parser import *
from engine.parser.parser import *
from engine.parser.yaml_parser import *
from engine.resolver.fs_resolver import FSPathResolver
from engine.data.context import SuiteContext
from engine.resolver.resolver_factory import *
from common.util.file_util import *
from engine.parser.parser_factory import ParserFactory
from engine.data.context import *

import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

## TODO: implement recursively, file regex check and
def invoke_all(file_path_loc,loc_type):
    pass

def invoke_single(file_path_loc,loc_type):
    ##context = SheetContext()

    file = ResolverFactory.get_resolver(loc_type).resolve(file_path_loc)

    file_ext = get_file_ext(file_path_loc)
    logger.info('Runner:invoke_single with file_extension %s',file_ext)
    sheet = ParserFactory.get_parser(file_ext).parse(file)

    ##context.initialize(sheet)

    result = ExecutorFactory().get_executor('XUnitStyle').execute(sheet)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('execution_type', type=str,choices=['execute-one','execute-all'],
                        help='execution type ')

    parser.add_argument('file_path_location', type=str,
                        help='file location / path')

    parser.add_argument('loc_type', type=str, choices = ['git','s3','fs'],
                        help='location type')


    args = parser.parse_args()

    execution_type = args.execution_type
    file_path_loc = args.file_path_location
    loc_type = args.loc_type

    if execution_type == 'execute-one':
        invoke_single(file_path_loc,loc_type)
    else:
        invoke_all(file_path_loc,loc_type)

##python runner.py execute-one /Users/deepak/PycharmProjects/rfk-sql-test-framework/running_config_be_step1_inventory.yml fs