from fastapi import APIRouter, Depends, Response, status
from auth.auth_bearer import JWTBearer
from db_conn.db import get_db_connection, close_connection
from models.user import UserId
from bson import ObjectId

router = APIRouter()

# /delete/user-- Endpoint to delete a user and tasks and notes created by the user
@router.post('/delete/user', status_code=200, description="Delete a user and all tasks and notes created by the user", tags=["query"], dependencies=[Depends(JWTBearer())])
async def delete_user(userId: UserId, response: Response):
    try:
        # print(userId.userId)
        client = get_db_connection()
        # Transaction to start a transaction, execute the callback, and commit (or abort on error).
        with client.start_session() as session:
            try:
                session.start_transaction()
                chain_delete(session, client, str(userId.userId)),
                session.commit_transaction()
                return {'Msg': "User deleted successfully" }, status.HTTP_200_OK
            except Exception as e:
                session.abort_transaction()
                raise Exception(e)
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'error': "Could not delete user."}, status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        close_connection(client)


# Function that deletes user, tasks and notes (transaction)
def chain_delete(session, client, userId):
    db = client["rb_database"]
    tasks = db.tasks
    notes = db.notes
    users = db.users
    resultsA = tasks.delete_many({"user": userId}, session=session)
    resultsB = notes.delete_many({"user": userId}, session=session)
    userId = ObjectId(userId)
    resultC = users.delete_one({"_id": userId}, session=session)
    # print(resultsA)
    # print(resultsB)
    # print(resultC)

