from fastapi import APIRouter, Depends, HTTPException, Response, status
from auth.auth_bearer import JWTBearer
from db_conn.db import get_db_connection
from models.note import Note

router = APIRouter()


# /note/create -- Endpoint to create a note, linked to a user
@router.post('/note/create', status_code=201, description="Create a note", tags=["note"], dependencies=[Depends(JWTBearer())])
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