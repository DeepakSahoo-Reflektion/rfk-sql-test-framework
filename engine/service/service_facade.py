import ntpath

from engine.service.db_service import *
from engine.service.service import *
from common.util.common_util import *
from common.const.vars import SQL_PATH,CONFIG_FILE_NAME,DOLLAR

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class ServiceFacade(object):
    '''
    Facade implementation of the service class where all the implementation details are abstracted away from the client
    code. A client program just have to call the serve method with the proper argument.
    '''

    def __init__(self, context):
        '''
        Initializes the parameters of the class.

        :param context:passed from the client program which is needed down the layer.
        '''
        self._db_service = DBService(context)
        self._context = context

    def _resolve_placeholder(self,arg):
        logger.info('ServiceFacade:_resolve_placeholder ENTRY with %s', arg)


        conf_file_name = ntpath.basename(self._context.kv[CONFIG_FILE_NAME])

        DEFAULT_INI_FILE_NAME=self._context.kv[SQL_PATH]+'/'+get_file_name_without_ext(conf_file_name)+'.ini'
        logger.info('ServiceFacade:_resolve_placeholder DEFAULT_INI_FILE_NAME with %s', DEFAULT_INI_FILE_NAME)
        sql_query = read_value_from_ini_file(DEFAULT_INI_FILE_NAME,arg[1:])
        logger.info('ServiceFacade:_resolve_placeholder EXIT with %s',sql_query)
        return sql_query

    def _evaluate_single(self, args):
        '''
        Evaluates a single SQL statement, script

        :param args: contains the SQL statement, script
        :return: the result of the SQL execution in terms of ([headers],[rows])
        '''
        if len(args) == 0:
            logger.warn('ServiceFacade:_evaluate_single empty args returning....')
            return

        sql = extract_qry_from(args)

        if get_input_sql_type(args) == 'sql_script':
            if "/" not in sql:
                sql = '/'.join((self._context.kv[SQL_PATH], sql))

        if sql.startswith('$'):
            logger.info('starts with dollar')
            sql = self._resolve_placeholder(sql)
        logger.info('ServiceFacade:_evaluate_single before calling the serve %s',sql)
        return self._db_service.serve(sql)

    def _evaluate_list(self, args):
        '''
        Calls the _evaulate_single() method for each argument.

        :param args: Takes a list of SQL statement or script for execution
        :return: The result in list of tuples of the SQL execution result
        '''
        ret = [self._evaluate_single(arg) for arg in args]

    def serve(self, args):
        '''
        facade method of the class. exposed to the client program.

        :param args: can be list of SQL statements or scripts or single SQL statement or script
        :return: the result of the SQL evaluation
        '''
        if isinstance(args, list):
            return self._evaluate_list(args)
        else:
            return self._evaluate_single(args)

    def close(self):
        logger.info('ServiceFacade:close...')
        self._db_service.close()
