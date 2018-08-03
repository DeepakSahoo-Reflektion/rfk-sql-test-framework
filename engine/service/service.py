import abc

from common.util.common_util import *


class Service(metaclass=abc.ABCMeta):
    '''
    ABC service class. As of now only one child implementation is there DBService.
    In future there can be more of them.
    '''

    @abc.abstractmethod
    def serve(self, args):
        pass
