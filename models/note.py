from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

class Note(BaseModel):
    userId: str           # user who create the note
    note : str            # the note

    @field_validator('userId')
    def validate_objectId(cls, user):
        try:
            ObjectId(str(user))
            return user
        except:
            raise ValueError('Invalid userId') 

class GetUserNote(BaseModel):
    userId: str
    page: int = Field(default=1, gt=0)
    limit: int = Field(default=10, gt=0)

    @field_validator('userId')
    def validate_objectId(cls, v):
        try:
            ObjectId(str(v))
            return v
        except:
            raise ValueError('Invalid userId')