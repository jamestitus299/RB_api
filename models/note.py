from pydantic import BaseModel, EmailStr, Field

class Note(BaseModel):
    user: str           # user who create the note
    note : str          # the note 

class GetUserNote(BaseModel):
    userId: str
    page: int = Field(default=1, gt=0)
    limit: int = Field(default=10, gt=0)