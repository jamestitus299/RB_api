import os
from pymongo import MongoClient

# import queue
#Connection pool 
# connection_pool = queue.Queue(maxsize=5)
# pool_created = False

# def create_pool():
#     global pool_created
#     if pool_created:
#         return
#     else:
#         for _ in range(5):
#             client = MongoClient(os.environ.get('MONGO_CONN_STRING'))
#             connection_pool.put(client)
#         pool_created = True


# create a MongoClient and return a connection client
def get_db_connection():
    # create_pool()
    # client = connection_pool.get()
    client = MongoClient(os.environ.get('MONGO_CONN_STRING'))
    return client

# mimics connections close (adds the connections back to the connectino pool)
def close_connection(client):
    # connection_pool.put(client)
    client.close()