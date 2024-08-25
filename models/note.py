from pydantic import BaseModel, EmailStr

class Note(BaseModel):
    user: str           # user who create the note
    note : str          # the note 

class GetUserNote(BaseModel):
    userId: str
    page : int | None = None
    limit: int | None = None 