import os
from pymongo import MongoClient

# create a MongoClient and return a connection to the database
def get_db_connection():
    client = MongoClient(os.environ.get('MONGO_CONN_STRING'), maxPoolSize=10)
    db = client["rb_database"]  # database name
    return db

