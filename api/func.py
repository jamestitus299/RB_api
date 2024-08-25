from fastapi import APIRouter, Depends, Response, status
from auth.auth_bearer import JWTBearer
from db_conn.db import get_db_connection, close_connection
from models.response import BaseResponse, ErrorResponse
from models.user import UserId
from bson import ObjectId

router = APIRouter()

# /delete/user-- Endpoint to delete a user and tasks and notes created by the user
@router.post('/delete/user', status_code=200, response_model=BaseResponse|ErrorResponse , description="Delete a user and all tasks and notes created by the user", tags=["query"], dependencies=[Depends(JWTBearer())])
async def delete_user(userId: UserId, response: Response):
    try:
        client = get_db_connection() 
        # check if user exists
        user_exist = check_user_exist(client, str(userId.userId))
        if(user_exist is None):
            response.status_code = 404
            return ErrorResponse(error="User dosen't exist")
        
        # Transaction to start a transaction, execute the callback, and commit (or abort on error).
        with client.start_session() as session:
            try: 
                session.start_transaction()
                chain_delete(session, client, str(userId.userId))
                session.commit_transaction()
                return BaseResponse(msg="User deleted successfully")
            except Exception as e:
                session.abort_transaction()
                response.status_code = 503
                return ErrorResponse(error="Could not delete User")
    except Exception as e:
        print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Serval Error")
    finally:
        close_connection(client)


# Function that deletes user, tasks and notes (transaction)
def chain_delete(session, client, userId):
    """
        deletes the tasks and notes created by the user, and then deletes the user also
    """
    db = client["rb_database"]
    tasks = db.tasks
    notes = db.notes
    users = db.users
    resultsA = tasks.delete_many({"user": ObjectId(userId)}, session=session)
    resultsB = notes.delete_many({"user": ObjectId(userId)}, session=session)
    resultC = users.delete_one({"_id": ObjectId(userId)}, session=session)
    print(resultsA)
    print(resultsB)
    print(resultC)

# # Checks if the user exists in the database
def check_user_exist(client, userId):
    """
        checks if the user exists in the database, return the result of the find_one query by userId
    """
    db = client["rb_database"]
    users = db.users
    user_exist = users.find_one({"_id": ObjectId(userId)}, {"_id: 1"})
    return user_exist

