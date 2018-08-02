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
from common.const.vars import SHEET,SUITE

import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def invoke(exec_type,file_path_loc,loc_type):
    context = ContextManager.initialize_default(SHEET)

    file_ext = get_file_ext(file_path_loc)

    file = ResolverFactory.get_resolver(loc_type).resolve(file_path_loc)

    sheet = ParserFactory.get_parser(file_ext).parse(file)

    context.update_params(sheet)

    result = ExecutorFactory.get_executor(exec_type, context).execute(sheet)

    return result

## TODO: implement regex
def invoke_all(exec_type,file_path_loc,loc_type):
    for root, dirs, files in os.walk(file_path_loc):
        if files:
            for file in files:
                file_path = os.path.join(root, file)
                if file.startswith('test_'):
                    invoke(exec_type,file_path,loc_type)

def invoke_single(exec_type,file_path_loc,loc_type):
    # context = ContextManager.initialize_default(SUITE)
    #
    # context.add_sheet_context()
    invoke(exec_type,file_path_loc,loc_type)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('exec_strategy', type=str,choices=['execute-one','execute-all'],
                        help='execution type ')

    parser.add_argument('loc_type', type=str, choices = ['git','s3','fs'],
                        help='location type')

    parser.add_argument('exec_type', type=str, choices=['xunit', 'bdd'],
                        help='location type')

    parser.add_argument('file_path_location', type=str,
                        help='file location / path')

    args = parser.parse_args()

    exec_strategy = args.exec_strategy
    loc_type = args.loc_type
    exec_type = args.exec_type
    file_path_loc = args.file_path_location


    if exec_strategy == 'execute-one':
        invoke_single(exec_type,file_path_loc,loc_type)
    else:
        invoke_all(exec_type,file_path_loc,loc_type)

##python runner.py execute-one /Users/deepak/PycharmProjects/rfk-sql-test-framework/running_config_be_step1_inventory.yml fs
##python runner.py execute-one fs xunit /Users/deepak/PycharmProjects/rfk-sql-test-framework/running_config_be_step1_inventory.yml

## python runner.py execute-one fs xunit /Users/deepak/PycharmProjects/rfk-sql-test-framework/running_config_be_step1_inventory.json


## docker build -t rfk-sql-test-fw:1.0 .
