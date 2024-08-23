from fastapi import APIRouter, Depends, HTTPException, Response, status
from auth.auth_bearer import JWTBearer
from db_conn.db import get_db_connection
from models.note import Note
from models.user import UserId

router = APIRouter()


# /create -- Endpoint to create a note, linked to a user
@router.post('/create', status_code=201, description="Create a note", tags=["note"], dependencies=[Depends(JWTBearer())])
async def create_note(note: Note, response: Response):
    try:
        # print(user)
        db = get_db_connection()
        users = db.notes
        result = users.insert_one(note.model_dump())
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
    

# /user -- Endpoint to retrieve all notes created by a user
@router.post('/user', status_code=200, description="Retrieve notes created by user", tags=["note"], dependencies=[Depends(JWTBearer())])
async def get_user_note(userId: UserId, response: Response):
    try:
        # print(userId.userId)
        db = get_db_connection()
        tasks = db.notes
        userId = str(userId.userId)
        results = tasks.find({"user": userId}, {"note": 1, "_id": 0 }).limit(10)
        
        note_list = [note["note"] for note in results]    
        if not note_list:
            response.status_code = 404    
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User has no Note.")
        
        # print(note_list)
        return {'notes': note_list }, status.HTTP_200_OK
    except Exception as e:
        # print(e)
        response.status_code = 500
        return {'error': "Could not retrieve NOtes"}, status.HTTP_500_INTERNAL_SERVER_ERROR