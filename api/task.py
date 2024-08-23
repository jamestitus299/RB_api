from fastapi import APIRouter, Depends, HTTPException, Response, status
from auth.auth_bearer import JWTBearer
from db_conn.db import get_db_connection
from models.task import Task

router = APIRouter()

# /note/create -- Endpoint to create a task, linked to a user
@router.post('/create', status_code=201, description="Create a task", tags=["task"], dependencies=[Depends(JWTBearer())])
async def create_task(task: Task, response: Response):
    try:
        # print(user)
        db = get_db_connection()
        users = db.tasks
        result = users.insert_one(task.model_dump())
        inserted_id = str(result.inserted_id)

        if(result.acknowledged):
            response.status_code = 201
            return {'note': inserted_id, }, status.HTTP_201_CREATED
        else:
            response.status_code = 500
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not Create Task.")
    except Exception as e:
        # print(e)
        response.status_code = 500
        return {'error': "Could not create Task"}, status.HTTP_500_INTERNAL_SERVER_ERROR
