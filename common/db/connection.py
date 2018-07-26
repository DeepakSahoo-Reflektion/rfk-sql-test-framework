from common.db.snowflake_connection import SnowflakeConnection

class ConnectionFactory(object):

    def get_connection(self, db_type = 'Snowflake'):
        if db_type == 'Snowflake':
            return SnowflakeConnection().get_connection()
        else:
            return None
