
from fastapi import APIRouter, HTTPException, Response, status
from db_conn.db import get_db_connection, close_connection

router = APIRouter()

# /hello -- Endpoint to check if the API server and MongoDB database server(connection) is alive (status)
@router.get('/hello', status_code=200, description="Check if the API Server is alive(status)", tags=["status"])
async def hello(response: Response):  
    try:
        client = get_db_connection()
        db = client["rb_database"]
        result = db.command('serverStatus')
        if result:
            response.status_code = 200
            return {'msg': 'Hello from RB API!'}, status.HTTP_200_OK
        else:
            raise Exception
    except Exception as e:  
        # print(e)
        response.status_code = 500
        return {'error': "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        close_connection(client)