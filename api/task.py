from fastapi import APIRouter, Depends, HTTPException, Response, status
from auth.auth_bearer import JWTBearer
from db_conn.db import get_db_connection
from models.task import Task
from models.user import UserId

router = APIRouter()

# /create -- Endpoint to create a task, linked to a user
@router.post('/create', status_code=201, description="Create a task", tags=["task"], dependencies=[Depends(JWTBearer())])
async def create_task(task: Task, response: Response):
    try:
        # print(user)
        db = get_db_connection()
        tasks = db.tasks
        result = tasks.insert_one(task.model_dump())
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
    

# /user -- Endpoint to retrieve all tasks created by a user
@router.post('/user', status_code=200, description="Retrieve tasks created by user", tags=["task"], dependencies=[Depends(JWTBearer())])
async def get_user_task(userId: UserId, response: Response):
    try:
        # print(userId.userId)
        db = get_db_connection()
        tasks = db.tasks
        userId = str(userId.userId)
        results = tasks.find({"user": userId}, {"task": 1, "_id": 0 }).limit(10)
        
        task_list = [task["task"] for task in results]    
        if len(task_list) == 0:
            response.status_code = 404
            return {'error': "User has no Tasks"}, status.HTTP_404_NOT_FOUND
        
        # print(task_list)
        return {'tasks': task_list }, status.HTTP_200_OK
    except Exception as e:
        # print(e)
        response.status_code = 500
        return {'error': "Could not retrieve Task"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    

