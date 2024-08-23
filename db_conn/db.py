import os
from pymongo import MongoClient

def get_db_connection():
    client = MongoClient(os.environ.get('MONGO_CONN_STRING'), maxPoolSize=10)
    # database name
    db = client["rb_database"]
    return db

