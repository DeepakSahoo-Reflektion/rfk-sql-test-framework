import abc

class Connection(metaclass=abc.ABCMeta):
    '''
    Interface of the Connection wrapper.
    SnowflakeConnection class is a child implementation of this interface.
    '''

    @abc.abstractmethod
    def get_connection(self, *args, **kwargs):
        '''
        Abstract method needs to be overriden in the child class. Must return their native
        connection.
        :param args:
        :param kwargs:
        :return:
        '''
        pass
