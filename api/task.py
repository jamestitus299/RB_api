import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response, status, Depends
from fastapi_pagination import Page, Params
from auth.auth_bearer import JWTBearer
from db_conn.db import get_db_connection, close_connection
from models.response import AdminTaskResponse, ErrorResponse, TaskCreatedResponse, UserTaskResponse
from models.task import GetUserTask, Task

router = APIRouter()

# /create -- Endpoint to create a task, linked to a user, requires valid jwt token (Bearer token)
@router.post('/create', status_code=201, response_model=TaskCreatedResponse|ErrorResponse, description="Create a task", tags=["task"], dependencies=[Depends(JWTBearer())])
async def create_task(task: Task, response: Response):
    try:
        # print(user)
        client = get_db_connection()
        db = client["rb_database"]
        tasks = db.tasks
        task_value = {
            "user" : ObjectId(task.user),
            "task" : task.task,
            "createdAt": datetime.datetime.utcnow()
        }
        result = tasks.insert_one(task_value)
        inserted_id = str(result.inserted_id)

        if(result.acknowledged):
            return TaskCreatedResponse(task=inserted_id)
        else:
            response.status_code = 503
            return ErrorResponse(error="Could not create Task.")
    except Exception as e:
        # print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Server Error")
    finally:
        close_connection(client)
    

# /user -- Endpoint to retrieve all tasks created by a user
@router.post('/user', status_code=200, response_model=UserTaskResponse|ErrorResponse, description="Retrieve tasks created by user", tags=["task"], dependencies=[Depends(JWTBearer())])
async def get_user_task(getUserTask: GetUserTask, response: Response):
    try:
        # print(userId.userId)
        client = get_db_connection()
        db = client["rb_database"]
        # check if the user exists
        users = db.users
        getUser = users.find_one({"_id": ObjectId(getUserTask.userId)})
        if getUser and getUser["userType"] != 1:
            response.status_code = 404
            return ErrorResponse(error="User does not exist")
        
        tasks = db.tasks
        # pagination
        page  = getUserTask.page if getUserTask.page else 1
        limit = getUserTask.limit if getUserTask.limit else 2      # default page size is 10
        skip = (page - 1) * limit
        results = tasks.find({"user": ObjectId(getUserTask.userId)}, {"task": 1, "_id": 0 }).sort("_id", 1).skip(skip).limit(limit)
        task_list = [task["task"] for task in results]    
        # print(task_list)
        res = UserTaskResponse(tasks=task_list)
        return res
    except Exception as e:
        # print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Server Error")
    finally:
        close_connection(client)
    

# /all -- Endpoint to retrieve all tasks, with the user who create it (join) (intended for use by admin )
@router.post('/all', status_code=200, response_model=AdminTaskResponse|ErrorResponse, description="Retrieve all tasks (only for admin user)", tags=["task"], dependencies=[Depends(JWTBearer())])
async def get_all_user_task(getTask: GetUserTask, response: Response):
    try:
        # print(userId.userId)
        client = get_db_connection()
        userId = str(getTask.userId)
        db = client["rb_database"]
        users = db.users
        
        # check if the user is Admin user
        getUser = users.find_one({"_id": ObjectId(userId)})
        if getUser and getUser["userType"] != 1:
            response.status_code = 403
            return ErrorResponse(error="Access Forbidden")

        # pagination
        page  = getTask.page if getTask.page else 1
        limit = getTask.limit if getTask.limit else 5  # default page size 10
        skip = (page - 1) * limit
        tasks = db.tasks
        # Perform the join using $lookup pipeline (join tasks on users)
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
            },
            {
            "$sort": {
                "_id": 1  # Sort by orderId in ascending order
                }
            },
            {
                "$skip": skip
            },
            {
                "$limit": limit
            }
        ]

        # Execute the aggregation pipeline
        results = tasks.aggregate(pipeline)
        # for document in results:
        #     print(document)
        #     print(type(document))

        task_list = [task for task in results]            
        # print(task_list)
        res = AdminTaskResponse(tasks=task_list)
        return res
    except Exception as e:
        print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Server Error")
    finally:
        close_connection(client)
