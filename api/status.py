
from fastapi import APIRouter, HTTPException, Response                                                                                                                                         
from db_conn.db import get_db_connection, close_connection
from models.response import BaseResponse, ErrorResponse

router = APIRouter()

# /hello -- Endpoint to check if the API server and MongoDB database server(connection) is alive (status)
@router.get('/hello', status_code=200, description="Check if the API Server is alive(status)", tags=["status"], response_model=BaseResponse|ErrorResponse)
async def hello(response: Response):
    try:
        client = get_db_connection()
        result = client.list_database_names()
        # print(result)
        if result and "rb_database" in result:
            res = BaseResponse(msg="Hello from RB API!")
            return res
        else:
            response.status_code = 500
            return ErrorResponse(error="Server Down")
    except Exception as e:  
        print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Server Error")
    finally:
        close_connection(client)