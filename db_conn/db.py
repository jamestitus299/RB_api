import os
from pymongo import MongoClient

# create a MongoClient and return a connection to the database
def get_db_connection():
    client = MongoClient(os.environ.get('MONGO_CONN_STRING'), maxPoolSize=10)
    db = client["rb_database"]  # database name
    return db


# create a MongoClient and return a client
def get_db_client():
    client = MongoClient(os.environ.get('MONGO_CONN_STRING'), maxPoolSize=10)
    return client

