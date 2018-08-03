from common.const.vars import SNOWFLAKE
from common.db.snowflake_connection import SnowflakeConnection

class ConnectionFactory(object):
    '''
    Factory class for returning connection objects. As of now only Snowflake connection is supported.
    In future can be enhanced for other connections also.
    '''

    @staticmethod
    def get_connection(db_type=SNOWFLAKE):
        '''
        Static factory method to return connection object based on the db_type.
        :param db_type: a string value based on which appropriate connection object will be returned
        :return: Connection type
        '''
        if db_type == SNOWFLAKE:
            return SnowflakeConnection().get_connection()
        else:
            return None