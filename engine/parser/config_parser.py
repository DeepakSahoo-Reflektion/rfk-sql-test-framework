from abc import *

class ConfigParser(ABC):

    @abstractmethod
    def parse(self, file_loc):
        pass

