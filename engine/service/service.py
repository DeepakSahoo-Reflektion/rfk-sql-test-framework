import logging
import abc

from common.util.file_util import *
from common.util.common_util import *
from common.db.connection import ConnectionFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Service(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def serve(self, args):
        pass


class DBService(Service):
    ## TODO : connection initialization and closing
    def __init__(self):
        logger.info('DBService:init block')
        self._conn = ConnectionFactory.get_connection('Snowflake')

        self._sql_expr_eval_map = {
            'statement': 'run_statement',
            'sql_script': 'run_script',
            'statment_placeholder': 'run_statement_placeholder'
        }

    ## TODO :try/catch with exception handling
    def run_script(self, script):
        logger.info('DBService:run_script script_file:%s', script)

        f = read_file(script)
        for cur in self._conn.execute_stream(f):
            for ret in cur:
                pass
        cur.close()

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
        ## TODO : call resolve_placeholder() and after that
        self.run_statement(statement)

    def serve(self, args):
        logger.info('DBService:Serve with args:%s', args)
        sql_exec_type = get_input_sql_type(args)

        func_type = self._sql_expr_eval_map[sql_exec_type]
        logger.info('DBService:Serve with func_type %s',func_type)
        try:
            func = get_function_by_name(self,func_type)
            ret = func(args)
        except AttributeError as e:
            logger.error('Attribute Error')
            raise e
        return ret

    def close(self):
        logger.info('Close the connections')
        try:
            self._conn.close()
        except:
            logger.error('Error closing connections')
            raise Exception('Error closing DB connection')