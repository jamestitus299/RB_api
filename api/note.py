import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, Response
from auth.auth_bearer import JWTBearer
from db_conn.db import get_db_connection, close_connection
from models.note import GetUserNote, Note
from models.response import ErrorResponse, NoteCreatedResponse, UserNoteResponse, AdminNoteResponse

router = APIRouter()

# /create -- Endpoint to create a note, linked to a user
@router.post('/create', status_code=201, response_model= NoteCreatedResponse|ErrorResponse, description="Create a note", tags=["note"], dependencies=[Depends(JWTBearer())])
async def create_note(note: Note, response: Response):
    try:
        # print(user)
        client = get_db_connection()
        db = client["rb_database"]
        users = db.notes
        note_value = {
            "user" : note.userId,
            "note" : note.note,
            "createdAt": datetime.datetime.utcnow()
        }
        result = users.insert_one(note_value)
        inserted_id = str(result.inserted_id)

        if(result.acknowledged):
            res = NoteCreatedResponse(note = inserted_id)
            return res
        else:
            response.status_code = 503
            return ErrorResponse(error="Could not create Note")
    except Exception as e:
        # print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Server Error")
    finally:
        close_connection(client)
    

# /user -- Endpoint to retrieve all notes created by a user
@router.post('/user', status_code=200, response_model=UserNoteResponse|ErrorResponse, description="Retrieve notes created by user", tags=["note"], dependencies=[Depends(JWTBearer())])
async def get_user_note(getUserNote: GetUserNote, response: Response):
    try:
        # print(userId.userId)
        client = get_db_connection()
        db = client["rb_database"]
        # check if the user exists
        users = db.users
        getUser = users.find_one({"_id": ObjectId(getUserNote.userId)})
        if not getUser:
            response.status_code = 404
            return ErrorResponse(error="User does not exist")
        
        notes = db.notes
        # pagination
        page  = getUserNote.page if getUserNote.page else 1        # default is page 1
        limit = getUserNote.limit if getUserNote.limit else 2      # default limit is 10
        skip = (page - 1) * limit
        results = notes.find({"user": ObjectId(getUserNote.userId)}, {"note": 1, "_id": 0 }).sort("createdAt", -1).skip(skip).limit(limit)
        note_list = [note["note"] for note in results]    
        # print(task_list)
        res = UserNoteResponse(notes=note_list)
        return res
    except Exception as e:
        # print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Server Error")
    finally:    
        close_connection(client)


# /all -- Endpoint to retrieve all notes, with the user who create it (join) (intended for use by admin )
@router.post('/all', status_code=200, response_model=AdminNoteResponse|ErrorResponse , description="Retrieve all notes (only for admin user)", tags=["note"], dependencies=[Depends(JWTBearer())])
async def get_all_user_note(getNote: GetUserNote, response: Response):
    try:
        # print(userId.userId)
        userId = str(getNote.userId)
        client = get_db_connection()
        db = client["rb_database"]
        users = db.users

        # check if the user is Admin user
        getUser = users.find_one({"_id": ObjectId(userId)})
        if not getUser or getUser["userType"] != 1:
            response.status_code = 403
            return ErrorResponse(error="Access Forbidden")

        # pagination
        page  = getNote.page if getNote.page else 1
        limit = getNote.limit if getNote.limit else 5  # default page size 10
        skip = (page - 1) * limit
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
            },
            {
            "$sort": {
                "createdAt": -1  # Sort by orderId in descending order
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
        results = notes.aggregate(pipeline)
        # for document in results:
        #     print(document)

        note_list = [note for note in results]        
        # print(note_list)
        res = AdminNoteResponse(notes=note_list)
        return res
    except Exception as e:
        print(e)
        response.status_code = 500
        return ErrorResponse(error="Internal Server Error")
    finally:
        close_connection(client)