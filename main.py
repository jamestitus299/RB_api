
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from flask import Flask, jsonify
from fastapi import FastAPI, Form, HTTPException, Request, status

from models.user import User
from db_conn.db import get_db_connection
from utils.password_security import encrypt_password, check_encrypted_password

load_dotenv()

# App
# app = Flask(__name__)
app = FastAPI()


# /hello -- Endpoint to check if the MongoDB database server is alive
@app.get('/hello')
async def hello():  
    try:
        db = get_db_connection()
        result = db.command('serverStatus')
        if result:
            return {'message': 'Hello from RB API!'}, status.HTTP_200_OK
        else:
            return {'message': "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:  
        print(e)  
        return {'message': "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR



# /user/register -- Endpoint to create a user, accepts only application/json data as per the User data model
@app.post('/user/register')
async def register(user:User):
    try:
        # print(user)
        user.password = encrypt_password(user.password)
        # print(check_encrypted_password(user.password, "$pbkdf2-sha256$30000$5/yf8x6j1JpTylkLoXQuZQ$..Es.Hj/Rs.7JNzE8KBTaYeGi8QDqL9jr0JoAJ1vl/g"))
        db = get_db_connection()
        users = db.users
        result = users.insert_one(user.model_dump())
        inserted_id = str(result.inserted_id)

        if(result.acknowledged):
            return {'user': inserted_id}, status.HTTP_201_CREATED
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not Create User.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

    
@app.exception_handler(HTTPException)
async def custom_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content={"Error detail": exc.detail},
        status_code=exc.status_code
    )


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))   
    
