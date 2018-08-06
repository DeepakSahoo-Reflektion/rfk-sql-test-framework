import logging
import argparse

from common.util.file_util import *
from common.const.vars import *

from engine.executor.executor_factory import ExecutorFactory
from engine.resolver.resolver_factory import *
from engine.parser.parser_factory import ParserFactory
from engine.data.context import *

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


def _invoke_sheet(sheet_context):
    sheet_context.update_params({FILE_EXT: get_file_ext(sheet_context.get_param(FILE_PATH_LOC))})

    file = ResolverFactory.get_resolver(sheet_context).resolve(
        sheet_context.get_param(FILE_PATH_LOC))

    sheet = ParserFactory.get_parser(sheet_context).parse(file)
    sheet_context.update_data(sheet)

    result = ExecutorFactory.get_executor(sheet_context).execute(sheet_context)

    return sheet_context


def _invoke_all(suite_context):
    for root, dirs, files in os.walk(suite_context.get_params(FILE_PATH_LOC)):
        if files:
            for file in files:
                file_path = os.path.join(root, file)
                if file.startswith('test_'):
                    _invoke_sheet(suite_context)


def _invoke_single(suite_context):
    sheet_context = ContextManager.initialize_default(SHEET)
    sheet_context.update_params(
        suite_context.get_params([LOC_TYPE, EXEC_TYPE, FILE_PATH_LOC]))

    suite_context.update_contexts({'Context-1': _invoke_sheet(sheet_context)})
    return suite_context


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
        _invoke_single(suite_context)
    else:
        _invoke_all(exec_type, file_path_loc, loc_type)
