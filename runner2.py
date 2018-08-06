import logging
import argparse

from common.const.vars import *
from engine.data.context import *
from engine.runner.execution_strategy import *

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()



if __name__ == '__main__':
    suite_context = ContextManager.initialize_default(SUITE)

    parser = argparse.ArgumentParser()
    parser.add_argument(EXEC_STRATEGY, type=str, choices=[EXECUTE_ONE, EXECUTE_ALL],
                        help='execution type ')

    parser.add_argument(LOC_TYPE, type=str, choices=[GIT, S3, FS],
                        help='location type')

    parser.add_argument(EXEC_TYPE, type=str, choices=[XUNIT, BDD],
                        help='location type')

    parser.add_argument(FILE_PATH_LOC, type=str,
                        help='file location / path')

    args = parser.parse_args()

    exec_strategy = args.exec_strategy
    loc_type = args.loc_type
    exec_type = args.exec_type
    file_path_loc = args.file_path_location

    suite_context.update_params(
        {EXEC_STRATEGY: exec_strategy, LOC_TYPE: loc_type, EXEC_TYPE: exec_type, FILE_PATH_LOC: file_path_loc})



    if exec_strategy == EXECUTE_ONE:
        execution_strategy = ExecuteOneStrategy(suite_context)
    else:
        execution_strategy = ExecuteAllStrategy(suite_context)
    execution_context = ExecutionContext(execution_strategy)
    execution_context.execute()
