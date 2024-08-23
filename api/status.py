
from fastapi import APIRouter, Depends, HTTPException, Response, status
from auth.auth_bearer import JWTBearer
from auth.jwt_auth import sign_jwt
from auth.password_security import check_encrypted_password, encrypt_password
from db_conn.db import get_db_connection

router = APIRouter()

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