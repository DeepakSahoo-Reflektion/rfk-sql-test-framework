import abc

class PathResolver(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def resolve(self,path):
        pass