import snowflake.connector
import os
import logging

from common.const.vars import SNOWFLAKE_ACC, SNOWFLAKE_USER, SNOWFLAKE_PWD
from common.db.connection import Connection

LOGGER = logging.getLogger(__name__)


class SnowflakeConnection(Connection):
    '''
    Wrapper class on top of snowflake native connector. Instead of using the snowflake connector directly
    this class provides interfaces to get the connection and close the connection.
    '''

    def __init__(self):
        '''
        Initialization block of the class. Intializes the connection object.
        Also performs validation on the params like USER,PWD and ACC.
        '''

        self._conn = None
        param_validation_rule = [not SNOWFLAKE_USER,
                                 not SNOWFLAKE_PWD,
                                 not SNOWFLAKE_ACC]

        if any(param_validation_rule):
            LOGGER.error('Missing Snowflake configuration')
            raise Exception('Missing Snowflake configuration')

    def _check_connection(self):
        '''
        helper method to check the client program is able to connect to snowflake warehouse or not.
        In case any error raises the exception
        :return:
        '''
        cs = self._conn.cursor()
        try:
            cs.execute("SELECT current_version()")
            one_row = cs.fetchone()
            LOGGER.info('Snowflake connection established successfully.. version:%s', one_row[0])
        except Exception as e:
            LOGGER.error('Failed to establish Snowflake connection %s', e.args)
            raise e
        finally:
            cs.close()

    def get_connection(self):
        '''
        Method which will be used by the client program to get the snowflake connection object.
        In case any error raises the exception.
        :return: Snowflake Connection object.
        '''
        try:
            self._conn = snowflake.connector.connect(
                user=SNOWFLAKE_USER,
                password=SNOWFLAKE_PWD,
                account=SNOWFLAKE_ACC
            )
            self._check_connection()
        except Exception as e:
            LOGGER.error('Failed to establish Snowflake connection ')
            raise e
        return self._conn

    def close(self):
        '''
        Method which will be called from the client program to close the connection object.
        :return:
        '''
        LOGGER.info('Closing the Snowflake Connection')
        try:
            self._conn.close()
        except Exception as e:
            LOGGER.error('Error closing snowflake connection')
            raise e
        finally:
            self._conn.close()
