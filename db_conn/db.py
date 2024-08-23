import os
from pymongo import MongoClient

# return the connection to the database
def get_db_connection():
    client = MongoClient(os.environ.get('MONGO_CONN_STRING'), maxPoolSize=10)
    # database name
    db = client["rb_database"]
    return db

