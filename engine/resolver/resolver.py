import abc


class PathResolver(metaclass=abc.ABCMeta):
    '''
    Abstract class of the Resolver type. Specifies that if you have to resolve any path eg:- s3,git or fs
    then provide your own implementation
    '''

    @abc.abstractmethod
    def resolve(self, path):
        '''
        Abstract method that each resolve implementation has to provide.
        take the path as argument and returns a file object
        :param path: path/string location
        :return: file
        '''
        pass
