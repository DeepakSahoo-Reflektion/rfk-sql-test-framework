from abc import *
from engine.executor.executor import *
from common.util.common_util import *

## TODO: dont create multiple instances of the Executor, return singleton objects
class ExecutorFactory:

    ## TODO : add the initialization code here for the factory
    def __init__(self,type = None):
        pass

    ##TODO : as we are returning none for invalid type make sure the client program checks it
    def get_executor(self,type):
        if not type:
            return

        if type == 'XUnitStyle':
            return XUnitStyleExecutor()

        elif type == 'BDDStyle':
            return BDDStyleExecutor()

class Executor(ABC):

    @abstractmethod
    def execute(self,sheet):
        pass

    @abstractmethod
    def close(self):
        pass


class BDDStyleExecutor(Executor):

    def execute(self,sheet):
        pass

class XUnitStyleExecutor(Executor):

    def __init__(self):
        self.conn = None
        self.attributes_list = ['after_each', 'after_once', 'before_each', 'before_once',
                           'name', 'sql_path', 'tests', 'validate']
        pass

    def close(self):
        pass

    def extract_attr(self,sheet):
        attributes_list = ['after_each', 'after_once', 'author', 'before_each', 'before_once', 'date', 'description', 'name', 'sql_path', 'tests', 'validate']
        pass

    def exec(self,sheet):
        before_once = sheet.__getattribute__('before_once')

        ret_value = self.run_script(before_once) if is_sql_script(before_once) else self.run_statments(before_once)


        pass

    ## TODO : improvise this below code
    def execute(self, sheet):
        print('inside execution of ',sheet)

        ## after_each', 'after_once', 'author', 'before_each', 'before_once', 'date',
        # 'description', 'name', 'sql_path', 'tests', 'validate'
        ##before_once = sheet.before_once1
        ##print(before_once)

        before_once = sheet.__getattribute__('before_once')
        print('++++',before_once)
        ##is_sql_script(before_once[0])
        pass

    def evaluate(self,arg):
        ret_value = self.run_script(arg) if is_sql_script(arg) else self.run_statments(arg)
        # if is_sql_script(arg):
        #     self.run_script(arg)
        # else:
        #     self.run_statments(arg)


        pass

    def run_script(self,script):
        pass

    def run_statment(self,statement):
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

    def close(self):
        print('close the connections and other objects')
        self.conn.close()

    ## TODO : manufacture the query here and proper asserts
    def execute_assert(self,each_assert):
        sql = each_assert.get('before_test',None)
        ret_value = self.run_script(sql) if is_sql_script(sql) else self.run_statments(sql)

        expected = each_assert.get('expected',None)
        ret_value = self.run_script(sql) if is_sql_script(sql) else self.run_statments(sql)

        pass

    def execute_test(self,test_case):
        try:
            before_test = test_case.get('before_test',None)
            ret_value = self.run_script(before_test) if is_sql_script(before_test) else self.run_statments(before_test)

            for each_assert in test_case.get('asserts'):
                self.execute_assert(each_assert)


            after_test = test_case.get('after_test',None)
            ret_value = self.run_script(after_test) if is_sql_script(after_test) else self.run_statments(after_test)

        except AttributeError as e:
            print('')

    def dummy(self,test_sheet):
        attributes_list = ['after_each', 'after_once', 'author', 'before_each', 'before_once', 'date', 'description',
                           'name', 'sql_path', 'tests', 'validate']


        try:
            before_once = test_sheet.__getattribute__('before_once')
            ret_value = self.run_script(before_once) if is_sql_script(before_once) else self.run_statments(before_once)

            for case in test_sheet.__getattribute__('tests'):
                before_each = test_sheet.__getattribute__('before_each')
                ret_value = self.run_script(before_each) if is_sql_script(before_each) else self.run_statments(
                    before_each)

                test_result = self.execute_test(case)

                after_each = test_sheet.__getattribute__('after_each')
                ret_value = self.run_script(after_each) if is_sql_script(after_each) else self.run_statments(after_each)

            after_once = test_sheet.__getattribute__('after_once')
            ret_value = self.run_script(after_once) if is_sql_script(after_once) else self.run_statments(after_once)

        except AttributeError as e:
            print('')
        pass




