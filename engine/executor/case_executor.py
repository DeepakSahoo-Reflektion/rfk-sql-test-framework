from abc import *

class Executor(ABC):

    @abstractmethod
    def execute(self,sheet):
        pass

class XUnitStyleExecutor(Executor):

    def execute(self,sheet):
        pass

class BDDStyleExecutor(Executor):

    def execute(self,sheet):
        pass

class ExecutorFactory:

    ## TODO : add the initialization code here
    def __init__(self,type = None):
        pass


    def get_executor(self,type):
        if not type:
            return

        if type == 'XUnitStyle':
            return XUnitStyleExecutor()

        elif type == 'BDDStyle':
            return BDDStyleExecutor()


