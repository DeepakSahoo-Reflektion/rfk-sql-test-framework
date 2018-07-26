from abc import *
import logging

from engine.executor.executor import *
from common.util.common_util import *
from engine.service.db_service import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


## TODO: dont create multiple instances of the Executor, return singleton objects
class ExecutorFactory:

    ## TODO : add the initialization code here for the factory
    def __init__(self,type = None):
        pass

    ##TODO : as we are returning none for invalid type make sure the client program checks it
    def get_executor(self,type):
        if not type:
            logger.error('ExecutorFactory: type is not provided')
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
        logger.info('XUnitStyleExecutor: Init')
        ##self.attributes_seq_stack = reversed(['before_once','before_each', 'tests','after_each','after_once'])
        self.attributes_seq_stack = ['after_once','after_each','tests','before_each','before_once']
        self.db_service = DBService()

    def extract_attributes(self,attr_name):
        try:
            func_name = self.__getattribute__(attr_name)
            return func_name
        except AttributeError as e:
            logger.warn('Missing Attribute', e)



    ## TODO : manufacture the query here and proper asserts
    def execute_assert(self, each_assert):
        sql = each_assert.get('sql', None)
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
            # before_once = test_sheet.__getattribute__('before_once')
            # ret_value = self.run_script(before_once) if is_sql_script(before_once) else self.run_statments(
            #     before_once)
            #self.service.execute(test_sheet.__getattribute__(self.attributes_seq_stack.pop()))
            self.service.execute(self.extract_attributes(self.attributes_seq_stack.pop()))


            for case in test_sheet.__getattribute__('tests'):
                # before_each = test_sheet.__getattribute__('before_each')
                # ret_value = self.run_script(before_each) if is_sql_script(before_each) else self.run_statments(
                #     before_each)
                self.service.execute(test_sheet.__getattribute__(self.attributes_seq_stack.pop()))

                test_result = self.execute_test(case)

                # after_each = test_sheet.__getattribute__('after_each')
                # ret_value = self.run_script(after_each) if is_sql_script(after_each) else self.run_statments(
                #     after_each)
                self.service.execute(test_sheet.__getattribute__(self.attributes_seq_stack.pop()))

            # after_once = test_sheet.__getattribute__('after_once')
            # ret_value = self.run_script(after_once) if is_sql_script(after_once) else self.run_statments(after_once)
            self.service.execute(test_sheet.__getattribute__(self.attributes_seq_stack.pop()))

        except AttributeError as e:
            print('')
        finally:
            logger.info('Closing the executor ')
            self.service.close()


     ## TODO : improvise this below code
    def execute(self, sheet):
        return self.execute_sheet(sheet)

