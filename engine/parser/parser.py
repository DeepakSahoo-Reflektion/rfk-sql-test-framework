import abc


class ConfigParser(metaclass=abc.ABCMeta):
    '''
    AbstractClass which specifies that you have to parse any type of file format, provide the implementatations.
    As of now there are 2 different implementation classes JsonParser and YamlParser.
    '''

    @abc.abstractmethod
    def parse(self, arg, **kwargs):
        '''
        The contract of the parse method. depends on the child classes implementations.
        :param arg:
        :param kwargs:
        :return:
        '''
        pass
