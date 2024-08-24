from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response, status
from auth.auth_bearer import JWTBearer
from db_conn.db import get_db_connection, close_connection
from models.task import Task
from models.user import UserId

router = APIRouter()

# /create -- Endpoint to create a task, linked to a user, requires valid jwt token (Bearer token)
@router.post('/create', status_code=201, description="Create a task", tags=["task"], dependencies=[Depends(JWTBearer())])
async def create_task(task: Task, response: Response):
    try:
        # print(user)
        client = get_db_connection()
        db = client["rb_database"]
        tasks = db.tasks
        task_value = {
            "user" : ObjectId(task.user),
            "task" : task.task
        }
        result = tasks.insert_one(task_value)
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
    finally:
        close_connection(client)
    

# /user -- Endpoint to retrieve all tasks created by a user
@router.post('/user', status_code=200, description="Retrieve tasks created by user", tags=["task"], dependencies=[Depends(JWTBearer())])
async def get_user_task(userId: UserId, response: Response):
    try:
        # print(userId.userId)
        client = get_db_connection()
        db = client["rb_database"]
        tasks = db.tasks
        results = tasks.find({"user": ObjectId(userId.userId)}, {"task": 1, "_id": 0 }).limit(10)
        
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
    finally:
        close_connection(client)
    

# /all -- Endpoint to retrieve all tasks, with the user who create it (join) (intended for use by admin )
@router.post('/all', status_code=200, description="Retrieve all tasks (only for admin user)", tags=["task"], dependencies=[Depends(JWTBearer())])
async def get_all_user_task(userId: UserId, response: Response):
    try:
        # print(userId.userId)
        userId = str(userId.userId)
        client = get_db_connection()
        db = client["rb_database"]
        users = db.users

        getUser = users.find_one({"_id": ObjectId(userId)})
        if getUser and getUser["userType"] != 1:
            response.status_code = 403
            return {"error": "Access Forbidden"}, status.HTTP_403_FORBIDDEN

        tasks = db.tasks
        # Perform the join using $lookup (join on tasks and users)
        pipeline = [
            {
                "$lookup": {
                    "from": "users",  # Local field to join on (user reference in tasks)
                    "localField": "user",  # Foreign field in tasks collection
                    "foreignField": "_id",  # Field in users collection to join on
                    "as": "user_info"  # Alias for the joined data
                }
            },
            {
                "$project": {
                    "task": 1,
                    "user_info.name": 1,
                    "user_info.email": 1,
                    "_id": 0
                }
            }
        ]

        # Execute the aggregation pipeline
        results = tasks.aggregate(pipeline)
        # for document in results:
            # print(document)

        task_list = [task for task in results]    
        if len(task_list) == 0:
            response.status_code = 404
            return {'error': "No Tasks"}, status.HTTP_404_NOT_FOUND
        
        # print(task_list)
        return {'tasks': task_list }, status.HTTP_200_OK
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'error': "Could not retrieve Tasks"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        close_connection(client)
