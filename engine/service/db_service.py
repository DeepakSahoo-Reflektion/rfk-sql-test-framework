import logging
import abc
from codecs import open

from common.util.file_util import *
from common.util.common_util import *
from common.db.connection_factory import ConnectionFactory
from engine.service.service import *

LOGGER = logging.getLogger(__name__)


class DBService(Service):
    '''
    Child implementation of the Service ABC. Mainly used for DB specific operations like - execution, get, update

    As of now only supports one operation. execution of the query.
    But in future this will be changed to accept one command object and from the command object what kind of execution
    will be determined.
    '''

    def __init__(self, context):
        '''
        Intialization of the DBService class.
        Initializes
            - context
            - connection object
            - sql_expression map
        :param context:
        '''
        self._conn = ConnectionFactory.get_connection('Snowflake')
        self._context = context
        self._sql_expr_eval_map = {
            'statement': 'run_statement',
            'sql_script': 'run_script',
            'statment_placeholder': 'run_statement_placeholder'
        }

    def run_script(self, script):
        '''
        Method for running any sql script

        :param script:
        :return: doesn't return any value
        '''
        LOGGER.info('EXECUTING:----------- %s', script)
        cur = self._conn.cursor()
        f = read_file(script)

        try:
            for cur in self._conn.execute_stream(f):
                for ret in cur:
                    pass
        except Exception as e:
            LOGGER.error('DBService:run_script error while executing the script %s', e.args)
            raise e
        finally:
            cur.close()
        LOGGER.debug('DBService:run_script EXIT')

    def run_statement(self, statement):
        '''
        Method used to execute any SQL statement

        :param statement: the SQL statement
        :return: the header and rows values if any.
        '''
        LOGGER.debug('DBService:run_statment ENTRY with :%s', statement)
        LOGGER.info('EXECUTING:----------- %s', statement)
        try:
            row_data = []
            headers = []

            cur = self._conn.cursor()
            row = cur.execute(statement)
            row_data = row.fetchall()

            if row is not None:
                headers = [i[0] for i in row.description]

            LOGGER.debug('DBService:run_statment EXIT headers:%s rows:%s', headers, row_data)
        except Exception as e:
            LOGGER.error('DBService:run_statment error which executing the sql', e.args)
            raise e
        finally:
            cur.close()
        return (headers, row_data)

    ## TODO: not yet implemented
    def run_statement_placeholder(self, statement):
        self.run_statement(statement)

    def _evaluate_single(self, args):
        '''
        Executes any SQL statement

        :param args: accepts the SQL statement as parameter
        :return:
        '''
        LOGGER.debug('DBService:_evaluate_single ENTRY with  %s', args)

        if len(args) == 0:
            LOGGER.warn('DBService:_evaluate_single empty args returning....')
            return

        sql_exec_type = get_input_sql_type(args)
        try:
            func_type = self._sql_expr_eval_map[sql_exec_type]
            func = get_function_by_name(self, func_type)
            ret = func(args)
        except AttributeError as e:
            LOGGER.error('DBService:_evaluate_single AttributeError %s', e.args)
            raise e
        except Exception as e:
            LOGGER.error('DBService:_evaluate_single Exception %s', e.args)
            raise e
        LOGGER.debug('DBService:_evaluate_single EXIT with  %s', ret)
        return ret

    def _evaluate_list(self, args):
        ret = [self._evaluate_single(arg) for arg in args]

    def serve(self, args):
        '''
        Entry point method of the class. Based on the parameter delegates the request to appropriate helper methods

        :param args:
        :return: result of the SQL execution
        '''
        if isinstance(args, list):
            return self._evaluate_list(args)
        else:
            return self._evaluate_single(args)

    def close(self):
        LOGGER.info('DBService:Close the connections')
        try:
            self._conn.close()
        except:
            LOGGER.error('DBService:Error closing connections')
            raise Exception('DBService:Error closing DB connection')
