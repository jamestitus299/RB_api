
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from fastapi import FastAPI, Form, HTTPException, Request, status
from pymongo import MongoClient

from models.user import User, UserResponse
from db_conn.db import get_db_connection

load_dotenv()

# Flask app
# app = Flask(__name__)
app = FastAPI()


@app.get('/hello')
async def hello():
    try:
        get_db_connection()
        return {'message': 'Hello from RB_API!'}, status.HTTP_200_OK
    except Exception as e:  
        print(e)  
        return {'message': "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.post('/register', response_model=UserResponse)
async def register(user:User):
    try:
        print(user)
        # db = get_db_connection()
        print(os.environ.get('MONGO_CONN_STRING'))
        # client = MongoClient(os.environ.get('MONGO_CONN_STRING'))
        # db = client["rb_database"]
        # users = db.users
        # result = users.insert_one(user.model_dump())

        # insertedUser = {result.inserted_id, user.name, user.email}

        return UserResponse.from_orm(user), status.HTTP_201_CREATED
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    



if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))   
    
