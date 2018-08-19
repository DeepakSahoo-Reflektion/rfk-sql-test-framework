import abc


class Generator(metaclass=abc.ABCMeta):
    '''
    ABC class for the Generator.
    child classes need to override the generate method
    '''

    @abc.abstractmethod
    def generate(self, data):
        '''
        Method where the actual execution of the engine starts.
        :param sheet:
        :return:
        '''
        pass
