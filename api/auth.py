from fastapi import APIRouter, Depends, HTTPException, Response, status
from auth.auth_bearer import JWTBearer
from auth.jwt_auth import sign_jwt
from auth.password_security import check_encrypted_password, encrypt_password
from db_conn.db import get_db_connection
from models.user import CreateUser, LoginUser

router = APIRouter()

# /user/register -- Endpoint to create a user, accepts only application/json data as per the User data model (unique use by email)
@router.post('/user/signup', status_code=201, description="Signup a new User", tags=["user"])
async def signup(user: CreateUser, response: Response):
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
            # generate jwt token and send it in the response
            jwt_token = sign_jwt(user.email)
            return {'user': inserted_id, 'access_token' : str(jwt_token["access_token"]) }, status.HTTP_201_CREATED
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not Create User.")
    except Exception as e:
        # print(e)
        response.status_code = 500
        return {'error': "Could not create User"}, status.HTTP_500_INTERNAL_SERVER_ERROR




# /user/login -- Endpoint to login, accepts only application/json data as per the User data model
@router.post('/user/login', status_code=200, description="Login a user", tags=["user"])
async def login(user: LoginUser, response: Response):
    try:
        db = get_db_connection()
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
            return {'Error':"Invalid Credentials"}, status.HTTP_403_FORBIDDEN
    except Exception as e:
        response.status_code = 500
        return {'Error':"Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR




# /hello -- Endpoint to check if the MongoDB database server is alive (status)
@router.get('/hello', status_code=200, description="Check if the Server is alive (status)", tags=["status"])
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
