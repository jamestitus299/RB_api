from pydantic import BaseModel, EmailStr

class Note(BaseModel):
    user: str           # user who create the note
    note : str          # the note 