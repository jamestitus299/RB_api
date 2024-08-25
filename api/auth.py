import datetime
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Response
from auth.jwt_auth import sign_jwt
from auth.password_security import check_encrypted_password, encrypt_password
from db_conn.db import get_db_connection, close_connection
from models.response import ErrorResponse, LoginResponse
from models.user import CreateAdminUser, CreateUser, LoginUser

load_dotenv()

router = APIRouter()

# /signup -- Endpoint to create a user, accepts only application/json data as per the User data model (an user is unique by email)
@router.post('/signup', status_code=201, description="Signup a new User", tags=["user"], response_model=LoginResponse | ErrorResponse)
async def signup(user: CreateUser, response: Response):
    try:
        # print(user)
        client = get_db_connection()
        db = client["rb_database"]
        users = db.users

        # Check if the user with email exists in the database
        already_exist = users.find_one({"email": user.email})
        if(already_exist is not None):
            response.status_code = 409
            return ErrorResponse(error="User already Exists")
        
        # if new user, then creater the user, password encrypted
        nUser = {
            "name": str(user.name),
            "email": str(user.email),
            "password" : str(encrypt_password(user.password)), 
            "userType" : 0,                                      # normal user is 0
            "createdAt": datetime.datetime.utcnow()
        }
        result = users.insert_one(nUser)
        inserted_id = str(result.inserted_id)

        if(result.acknowledged):
            # generate jwt token and send it in the response
            jwt_token = sign_jwt(user.email)
            res = LoginResponse(user=str(inserted_id), access_token=str(jwt_token["access_token"]))
            return res
        else:
            response.status_code = 503
            return ErrorResponse(error="Could not create User")
    except Exception as e:
        # print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Server Error")
    finally:
        close_connection(client)
    

# /signup/admin -- Endpoint to create an admin user, the admin should send a secret key along with the password in the request 
@router.post('/signup/admin', status_code=201, description="Signup an Admin User", tags=["user"], response_model=LoginResponse|ErrorResponse)
async def signup_admin(user: CreateAdminUser, response: Response):  

    # check secret key required for Admin registeration
    if user.secretKey != str(os.environ.get("ADMIN_SECRET_KEY")): 
        response.status_code = 401
        return ErrorResponse(error="Unauthorized Action") 
     
    try:
        # print(user)
        client = get_db_connection()
        db = client["rb_database"]
        users = db.users

        # Check if the user with email exists in the database
        already_exist = users.find_one({"email": user.email})
        if(already_exist is not None):
            response.status_code = 409
            return ErrorResponse(error="User already exists.")
        
        # if new admin user, then creater the admin user, password encrypted
        adminUser = {
            "name": str(user.name),
            "email": str(user.email),
            "password" : str(encrypt_password(user.password)), 
            "userType" : 1,                                    # Admin user is 1
            "createdAt": datetime.datetime.utcnow()
        }
        result = users.insert_one(adminUser)
        inserted_id = str(result.inserted_id)

        if(result.acknowledged):
            # generate jwt token and send it in the response
            jwt_token = sign_jwt(user.email)
            res = LoginResponse(user=str(inserted_id), access_token=str(jwt_token["access_token"]))
            return res
        else:
            response.status_code = 503
            return ErrorResponse(error="Could not create User")
    except Exception as e:
        print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Server Error")
    finally:
        close_connection(client)


# /user/login -- Endpoint to login, accepts only application/json data as per the LoginUser data model
@router.post('/login', status_code=200, description="Login a user", tags=["user"], response_model= LoginResponse|ErrorResponse)
async def login(user: LoginUser, response: Response):
    try:
        client = get_db_connection()
        db = client["rb_database"]
        users = db.users
        result = users.find_one({"email": user.email})

        if( result and check_encrypted_password(user.password, result["password"])):
            user_id = result["_id"]
            # generate jwt token and send it in the response
            jwt_token = sign_jwt(user.email)
            res = LoginResponse(user=str(user_id), access_token=str(jwt_token["access_token"]))
            return res
        else:
            response.status_code = 401
            return ErrorResponse(error="Invalid credentials")
    except Exception as e:
        print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Server Error")
    finally:
        close_connection(client)