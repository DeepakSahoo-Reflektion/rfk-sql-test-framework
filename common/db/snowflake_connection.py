import snowflake.connector
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class SnowflakeConnection:

    def __init__(self):
        self.snowflake_user = os.getenv('SNOWFLAKE_USER')
        self.snowflake_pwd = os.getenv('SNOWFLAKE_PWD')
        self.snowflake_acc = os.getenv('SNOWFLAKE_ACC')


        ## TODO : proper way of empty check and missing check and raise exceptions
        if not self.snowflake_user or not self.snowflake_pwd or not self.snowflake_acc:
            logging.error('MISSING SNOWFLAKE CONFIG')
            raise Exception('Missing Snowflake configuration')

    ## TODO : proper way of error handling and ping check if it can connect.
    def get_connection(self):
        try:
            self.conn = snowflake.connector.connect(
                user=self.snowflake_user,
                password=self.snowflake_pwd,
                account=self.snowflake_acc
            )
        except Exception:
            logging.error('Failed to establish Snowflake connection ')
            raise Exception('Failed to establish snowflake connection')
        return self.conn


    ## TODO: proper implementation
    def close(self):
        logger.info('Closing the SnowFlake Connections')
        try:
            self.conn.close()
        except Exception:
            logger.error('Error closing snowflake connection')
        finally:
            self.conn.close()
