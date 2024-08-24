import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response, status
from auth.jwt_auth import sign_jwt
from auth.password_security import check_encrypted_password, encrypt_password
from db_conn.db import get_db_connection, close_connection
from models.user import CreateAdminUser, CreateUser, LoginUser

load_dotenv()

router = APIRouter()

# /signup -- Endpoint to create a user, accepts only application/json data as per the User data model (an user is unique by email)
@router.post('/signup', status_code=201, description="Signup a new User", tags=["user"])
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
            return {'error': "User already exists. Try Logging in"}, status.HTTP_409_CONFLICT
        
        # if new user, then creater the user, password encrypted
        user.password = encrypt_password(user.password)
        user.userType = 0 # create a normal user
        result = users.insert_one(user.model_dump())
        inserted_id = str(result.inserted_id)

        if(result.acknowledged):
            response.status_code = 201
            # generate jwt token and send it in the response
            jwt_token = sign_jwt(user.email)
            return {'user': inserted_id, 'access_token' : str(jwt_token["access_token"]) }, status.HTTP_201_CREATED
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not Create User.")
    except Exception as e:
        # print(e)
        response.status_code = 500
        return {'error': "Could not create User"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        close_connection(client)
    

# /signup/admin -- Endpoint to create an admin user, the admin should send a secret key along with the password in the request 
@router.post('/signup/admin', status_code=201, description="Signup an Admin User", tags=["user"])
async def signup_admin(user: CreateAdminUser, response: Response):

    if user.secretKey != str(os.environ.get("ADMIN_SECRET_KEY")): # check secret key required for Admin registeration
        response.status_code = 403
        return {'error': "Could not create Admin"}, status.HTTP_403_FORBIDDEN
    
    try:
        # print(user)
        client = get_db_connection()
        db = client["rb_database"]
        users = db.users

        # Check if the user with email exists in the database
        already_exist = users.find_one({"email": user.email})
        if(already_exist is not None):
            response.status_code = 409
            return {'error': "User already exists. Try Logging in"}, status.HTTP_409_CONFLICT
        
        # if new admin user, then creater the admin user, password encrypted
        adminUser = {
            "name": str(user.name),
            "email": str(user.email),
            "password" : str(encrypt_password(user.password)), 
            "userType" : 1
        }
        result = users.insert_one(adminUser)
        inserted_id = str(result.inserted_id)

        if(result.acknowledged):
            response.status_code = 201
            # generate jwt token and send it in the response
            jwt_token = sign_jwt(user.email)
            return {'user': inserted_id, 'access_token' : str(jwt_token["access_token"]) }, status.HTTP_201_CREATED
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not Create User.")
    except Exception as e:
        # print(e)
        response.status_code = 500
        return {'error': "Could not create User"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        close_connection(client)




# /user/login -- Endpoint to login, accepts only application/json data as per the LoginUser data model
@router.post('/login', status_code=200, description="Login a user", tags=["user"])
async def login(user: LoginUser, response: Response):
    try:
        client = get_db_connection()
        db = client["rb_database"]
        users = db.users
        result = users.find_one({"email": user.email})

        if( result and check_encrypted_password(user.password, result["password"])):
            response.status_code = 200
            user_id = result["_id"]
            # generate jwt token and send it in the response
            jwt_token = sign_jwt(user.email)
            return {'user': str(user_id), 'access_token' : str(jwt_token["access_token"]) }, status.HTTP_200_OK
        else:
            response.status_code = 403
            return {'error':"Invalid Credentials"}, status.HTTP_403_FORBIDDEN
    except Exception as e:
        response.status_code = 500
        return {'error':"Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        close_connection(client)