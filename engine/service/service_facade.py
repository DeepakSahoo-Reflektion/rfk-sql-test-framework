from engine.service.db_service import *
from engine.service.fs_service import *
from engine.service.service import *
from common.util.common_util import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class ServiceFacade(object):

    def __init__(self, context):
        self._db_service = DBService(context)
        self._context = context

    def _evaluate_single(self,args):
        if len(args) == 0:
            logger.warn('ServiceFacade:Serve Empty args returning....')
            return

        logger.info('ServiceFacade:_evaluate_single with %s',args)
        loc_type = extract_loc_type(args)
        sql = extract_qry_from(args)
        sql_path = self._context.kv['sql_path']
        sql_exec_type = get_input_sql_type(args)
        logger.info('ServiceFacade:_evaluate_single with loc_type %s and sql %s and sql_path %s sql_exec_type %s', loc_type,sql,sql_path,sql_exec_type)




        if sql_exec_type == 'sql_script':
            if "/" not in sql:
                sql = '/'.join((self._context.kv['sql_path'], sql))


        logger.info('ServiceFacade:_evaluate_single after change sql %s', sql)
        return self._db_service.serve(sql)


    def _evaluate_list(self,args):
        logger.info('ServiceFacade:_evaluate_list ENTRY with  %s', args)
        ret = [self._evaluate_single(arg) for arg in args]
        logger.info('ServiceFacade:_evaluate_list EXIT with  %s', ret)


    def serve(self,args):
        if isinstance(args,list):
            return self._evaluate_list(args)
        else:
            return self._evaluate_single(args)


    def close(self):
        logger.info('ServiceFacade:close...')
        self._db_service.close()