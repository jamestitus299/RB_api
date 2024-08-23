
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from flask import Flask, jsonify
from fastapi import FastAPI, Form, HTTPException, Request, Response, status

from models.user import CreateUser, LoginUser
from db_conn.db import get_db_connection
from utils.password_security import encrypt_password, check_encrypted_password

load_dotenv()

# App
# app = Flask(__name__)
app = FastAPI()


# /hello -- Endpoint to check if the MongoDB database server is alive
@app.get('/hello')
async def hello(response: Response):  
    try:
        db = get_db_connection()
        result = db.command('serverStatus')
        if result:
            response.status_code = 200
            return {'message': 'Hello from RB API!'}, status.HTTP_200_OK
        else:
            raise HTTPException
    except Exception as e:  
        response.status_code = 500
        return {'message': "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR


# /user/register -- Endpoint to create a user, accepts only application/json data as per the User data model (unique use by email)
@app.post('/user/register', status_code=201)
async def register(user: CreateUser, response: Response):
    try:
        # print(user)
        db = get_db_connection()
        users = db.users

        # Check if the user with email exists in the database
        already_exist = users.find_one({"email": user.email})
        if(already_exist is not None):
            response.status_code = 409
            return {'error': "User already exists. Try Logging in"}, status.HTTP_409_CONFLICT
        
        # if new user, then creater the user, password encrypted
        user.password = encrypt_password(user.password)
        result = users.insert_one(user.model_dump())
        inserted_id = str(result.inserted_id)

        if(result.acknowledged):
            response.status_code = 201
            return {'user': inserted_id}, status.HTTP_201_CREATED
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not Create User.")
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'error': "Could not create User"}, status.HTTP_500_INTERNAL_SERVER_ERROR


# /user/login -- Endpoint to login, accepts only application/json data as per the User data model
@app.post('/user/login')
async def register(user: LoginUser, response: Response):
    try:
        db = get_db_connection()
        users = db.users
        result = users.find_one({"email": user.email})

        if( result and check_encrypted_password(user.password, result["password"])):
            response.status_code = 200
            return {'user': "User Logged in"}, status.HTTP_200_OK
        else:
            response.status_code = 403
            return {'Error':"Invalid Credentials"}, status.HTTP_403_FORBIDDEN
    except Exception as e:
        response.status_code = 500
        return {'Error':"Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))   
    
