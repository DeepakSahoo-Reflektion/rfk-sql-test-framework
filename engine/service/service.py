import logging
import abc
from codecs import open

from common.util.file_util import *
from common.util.common_util import *
from common.db.connection import ConnectionFactory

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class Service(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def serve(self, args):
        pass

