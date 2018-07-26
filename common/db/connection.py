import abc
from common.db.snowflake_connection import SnowflakeConnection

class ConnectionFactory(object):

    @staticmethod
    def get_connection(self, db_type = 'Snowflake'):
        if db_type == 'Snowflake':
            return SnowflakeConnection().get_connection()
        else:
            return None

class Connection(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_connection(self,*args,**kwargs):
        pass
