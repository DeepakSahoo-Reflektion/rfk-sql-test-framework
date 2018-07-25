from common.util.common_util import *

class GenericService:

    def execute(self,args):
        pass

class DBService(GenericService):

    def run_script(self, script):
        pass

    def run_statment(self, statement):
        try:
            cur = self.conn.cursor()
            row = cur.execute(statement)
            row_data = row.fetchall()
            ##print('before closing the cursor',row_data)

            if row == None:
                print('dont do anything')
            else:
                column_names = [i[0] for i in row.description]
                ##row_data = row.fetchall()
                ##print('middle closing the cursor', row_data)
                ##print('middle2 closing the cursor', row_data)


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


        sql_expr_eval_map = {
                                'statement': '',
                                'sql_script': '',
                                'statment_placeholder': ''
                             }


        pass







class DBCommand:

    def execute(self):
        pass

class