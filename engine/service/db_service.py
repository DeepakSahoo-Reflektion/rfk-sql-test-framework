from common.util.common_util import *
from common.config.snowflake_connection import SnowflakeConnection

class GenericService:

    def execute(self,args):
        pass

class DBService(GenericService):

    ## TODO : connection initialization and closing
    def __init__(self):
        self.conn = SnowflakeConnection().get_connection()
        pass


    def run_script(self, script):
        pass

    def run_statment(self, statement):
        try:
            cur = self.conn.cursor()
            row = cur.execute(statement)
            row_data = row.fetchall()

            if row == None:
                print('dont do anything')
            else:
                column_names = [i[0] for i in row.description]

        finally:
            cur.close()

        if row == None:
            return (None, None)
        else:
            # column_names = [i[0] for i in row.description]
            # row_data = row.fetchall()
            ##print('after execution', column_names, row_data)
            return (column_names, row_data)

    def execute(self,args):

        sql_exec_type = get_input_sql_type(args)

        sql_expr_eval_map = {
            'statement': 'run_statement',
            'sql_script': 'run_script',
            'statment_placeholder': 'run_statement_placeholder'
        }

        func_type = sql_expr_eval_map[sql_exec_type]

        try:
            func = self.__getattribute__(func_type)
            ret = func(args)
        except AttributeError:
            print('Attribute Error')

        return ret

    def close(self):
        print('Close the connections')
        try:
            self.conn.close()
        except:
            print('Error closing connections')
        pass