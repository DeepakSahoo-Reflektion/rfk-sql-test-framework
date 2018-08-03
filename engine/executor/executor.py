import abc


class Executor(metaclass=abc.ABCMeta):
    '''
    ABC class for the Executor.
    child classes need to override the execute method
    '''

    @abc.abstractmethod
    def execute(self, sheet):
        '''
        Method where the actual execution of the engine starts.
        :param sheet:
        :return:
        '''
        pass
