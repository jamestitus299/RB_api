
from fastapi import APIRouter, HTTPException                                                                                                                                         
from db_conn.db import get_db_connection, close_connection
from models.response import BaseResponse

router = APIRouter()

# /hello -- Endpoint to check if the API server and MongoDB database server(connection) is alive (status)
@router.get('/hello', status_code=200, description="Check if the API Server is alive(status)", tags=["status"], response_model=BaseResponse)
async def hello():
    try:
        client = get_db_connection()
        db = client["rb_database"]
        result = db.command('serverStatus')
        if result:
            res = BaseResponse(msg="Hello from RB API!")
            return res
        else:
            raise HTTPException(status_code=500, detail="Server Down")
    except Exception as e:  
        # print(e)
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    finally:
        close_connection(client)