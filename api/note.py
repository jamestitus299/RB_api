from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response, status
from auth.auth_bearer import JWTBearer
from db_conn.db import get_db_connection, close_connection
from models.note import Note
from models.user import UserId

router = APIRouter()

# /create -- Endpoint to create a note, linked to a user
@router.post('/create', status_code=201, description="Create a note", tags=["note"], dependencies=[Depends(JWTBearer())])
async def create_note(note: Note, response: Response):
    try:
        # print(user)
        client = get_db_connection()
        db = client["rb_database"]
        users = db.notes
        note_value = {
            "user" : ObjectId(note.user),
            "note" : note.note
        }
        result = users.insert_one(note_value)
        inserted_id = str(result.inserted_id)

        if(result.acknowledged):
            response.status_code = 201
            return {'note': inserted_id, }, status.HTTP_201_CREATED
        else:
            response.status_code = 500
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not Create Note.")
    except Exception as e:
        # print(e)
        response.status_code = 500
        return {'error': "Could not create Note"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        close_connection(client)
    

# /user -- Endpoint to retrieve all notes created by a user
@router.post('/user', status_code=200, description="Retrieve notes created by user", tags=["note"], dependencies=[Depends(JWTBearer())])
async def get_user_note(userId: UserId, response: Response):
    try:
        # print(userId.userId)
        client = get_db_connection()
        db = client["rb_database"]
        tasks = db.notes
        userId = str(userId.userId)
        results = tasks.find({"user": userId}, {"note": 1, "_id": 0 }).limit(10)
        
        note_list = [note["note"] for note in results]

        if len(note_list) == 0:
            response.status_code = 404
            return {'error': "User has no Notes"}, status.HTTP_404_NOT_FOUND
        
        return {'notes': note_list }, status.HTTP_200_OK
    except Exception as e:
        # print(e)
        response.status_code = 500
        return {'error': "Could not retrieve Notes"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        close_connection(client)


# /all -- Endpoint to retrieve all notes, with the user who create it (join) (intended for use by admin )
@router.post('/all', status_code=200, description="Retrieve all notes (only for admin user)", tags=["note"], dependencies=[Depends(JWTBearer())])
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

        notes = db.notes
        # Perform the join using $lookup pipeline (join notes on users)
        pipeline = [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user", 
                    "foreignField": "_id",  
                    "as": "user_info"  
                }
            },
            {
                "$project": {
                    "note": 1,
                    "user_info.name": 1,
                    "user_info.email": 1,
                    "_id": 0
                }
            }
        ]

        # Execute the aggregation pipeline
        results = notes.aggregate(pipeline)
        # for document in results:
        #     print(document)

        note_list = [note for note in results]    
        if len(note_list) == 0:
            response.status_code = 404
            return {'msg': "No Notes"}, status.HTTP_404_NOT_FOUND
        
        # print(note_list)
        return {'notes': note_list }, status.HTTP_200_OK
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'error': "Could not retrieve Tasks"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        close_connection(client)