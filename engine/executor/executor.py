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


class BDDStyleExecutor(Executor):

    def execute(self,sheet):
        pass


class XUnitStyleExecutor(Executor):

    ## TODO : make the attributes_list as a stack and pop the attributes in order till the stack is empty and invoke
    ## each corresponding method
    def __init__(self):
        self.attributes_seq_stack = reversed(['before_once','before_each', 'tests','after_each','after_once'])


    ## TODO : manufacture the query here and proper asserts
    def execute_assert(self, each_assert):
        sql = each_assert.get('before_test', None)
        ret_value = self.run_script(sql) if is_sql_script(sql) else self.run_statments(sql)

        expected = each_assert.get('expected', None)
        ret_value = self.run_script(sql) if is_sql_script(sql) else self.run_statments(sql)



    def execute_test(self, test_case):
        try:
            before_test = test_case.get('before_test', None)
            ret_value = self.run_script(before_test) if is_sql_script(before_test) else self.run_statments(
                before_test)

            for each_assert in test_case.get('asserts'):
                self.execute_assert(each_assert)

            after_test = test_case.get('after_test', None)
            ret_value = self.run_script(after_test) if is_sql_script(after_test) else self.run_statments(after_test)

        except AttributeError as e:
            print('')

    def execute_sheet(self, test_sheet):
        try:
            before_once = test_sheet.__getattribute__('before_once')
            ret_value = self.run_script(before_once) if is_sql_script(before_once) else self.run_statments(
                before_once)

            for case in test_sheet.__getattribute__('tests'):
                before_each = test_sheet.__getattribute__('before_each')
                ret_value = self.run_script(before_each) if is_sql_script(before_each) else self.run_statments(
                    before_each)

                test_result = self.execute_test(case)

                after_each = test_sheet.__getattribute__('after_each')
                ret_value = self.run_script(after_each) if is_sql_script(after_each) else self.run_statments(
                    after_each)

            after_once = test_sheet.__getattribute__('after_once')
            ret_value = self.run_script(after_once) if is_sql_script(after_once) else self.run_statments(after_once)

        except AttributeError as e:
            print('')


     ## TODO : improvise this below code
    def execute(self, sheet):
        return self.execute_sheet(sheet)

