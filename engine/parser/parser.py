import abc


class ConfigParser(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def parse(self, arg,**kwargs):
        pass




