import logging
import abc
from codecs import open

from common.util.file_util import *
from common.util.common_util import *
from common.db.connection import ConnectionFactory

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class Service(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def serve(self, args):
        pass

## TODO : connection initialization and closing
## TODO : call resolve_placeholder() and after that in run_statement_placeholder()
## TODO: Don't hardcode snowflake here, take it as parameter
## TODO :try/catch with exception handling inside run_script() and other methods
## TODO: fix logging
class DBService(Service):

    def __init__(self):
        logger.info('DBService:init block')
        self._conn = ConnectionFactory.get_connection('Snowflake')

        self._sql_expr_eval_map = {
            'statement': 'run_statement',
            'sql_script': 'run_script',
            'statment_placeholder': 'run_statement_placeholder'
        }


    def run_script(self, script):
        logger.info('DBService:run_script ENTRY script_file:%s', script)

        cur = self._conn.cursor()
        #row = cur.execute('USE TEST')
        # row = cur.execute("SET DATE='20180723'")
        # row = cur.execute("SET HOUR='03'")

        logger.info('DBService:run_script MIDDLE')
        f = read_file(script)

        # with open(script, 'r', encoding='utf-8') as f:
        #     for _cur in self._conn.execute_stream(f):
        #         for ret in _cur:
        #             print(ret)

        # with open(script, 'r', encoding='utf-8') as f:
        #     logger.info('inside run_script with %s',f)
        #     for cur in self._conn.execute_stream(f):
        #         for ret in cur:
        #             pass

        logger.info('DBService:run_script script_file:%s', f)
        for cur in self._conn.execute_stream(f):
            for ret in cur:
                #print(ret)
                pass

        cur.close()
        logger.info('DBService:run_script EXIT script_file:%s', script)

    def run_statement(self, statement):
        try:
            logger.info('DBService:run_statment ENTRY with args:%s', statement)

            row_data = []
            headers = []

            cur = self._conn.cursor()
            row = cur.execute(statement)
            row_data = row.fetchall()

            if row is not None:
                headers = [i[0] for i in row.description]

            logger.info('DBService:run_statment EXIT headers:%s rows:%s', headers, row_data)
        finally:
            cur.close()
        return (headers, row_data)

    def run_statement_placeholder(self, statement):
        self.run_statement(statement)


    def _evaluate_single(self,args):
        logger.info('DBService:_evaluate_single ENTRY with  %s', args)

        if len(args) == 0:
            logger.warn('DBService:Serve Empty args returning....')
            return

        sql_exec_type = get_input_sql_type(args)
        try:
            func_type = self._sql_expr_eval_map[sql_exec_type]
            logger.info('DBService:_evaluate_single with func_type %s', func_type)

            func = get_function_by_name(self, func_type)
            ret = func(args)
        except AttributeError as e:
            logger.error('DBService:_evaluate_single AttributeError..... %s', e.args)
            raise e
        except Exception as e:
            logger.error('DBService:_evaluate_single Exception %s', e.args)
            raise e
        logger.info('DBService:_evaluate_single EXIT with  %s', ret)
        return ret

    def _evaluate_list(self,args):
        logger.info('DBService:_evaluate_list ENTRY with  %s', args)
        ret = [self._evaluate_single(arg) for arg in args]
        logger.info('DBService:_evaluate_list EXIT with  %s', ret)


    def serve(self, args):
        logger.info('DBService:Serve ENTRY with args:%s', args)

        if isinstance(args,list):
            logger.info('DBService:Serve with list args')
            return self._evaluate_list(args)
        else:
            logger.info('DBService:Serve with single arg')
            return self._evaluate_single(args)


    def close(self):
        logger.info('DBService:Close the connections')
        try:
            self._conn.close()
        except:
            logger.error('DBService:Error closing connections')
            raise Exception('DBService:Error closing DB connection')