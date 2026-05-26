from psycopg2 import pool
import os

class Database:
    def __int__(self):
        host = os.getenv('DB_HOSTNAME')
        database_name = os.getenv('DB_NAME')
        user_name = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')
        connection_pool = pool.SimpleConnectionPool(minconn=2,
                                                    maxconn=10,
                                                    host=host,
                                                    user=user_name,
                                                    dbname=database_name,
                                                    password=password)


