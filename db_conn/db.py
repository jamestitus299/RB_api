import os
from pymongo import MongoClient
import queue

# Connection pool 
pool_number = 10
connection_pool = queue.Queue(maxsize=pool_number)
pool_created = False

def create_pool():
    global pool_created
    if pool_created:
        return
    else:
        for _ in range(pool_number):
            client = MongoClient(os.environ.get('MONGO_CONN_STRING'))
            connection_pool.put(client)
        pool_created = True


# creates a MongoClient and return a connection client
def get_db_connection():
    """
        gets a connection to the MongoDB database
    """
    create_pool()
    client = connection_pool.get() # gets a client connection from the connection pool
    return client

# closes the Client connection
def close_connection(client):
    """
        closes the connection to the MongoDB database
    """
    connection_pool.put(client) # mimics connections close (adds the connections back to the connectino pool)