from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator

class Task(BaseModel):
    userId: str           # user who create the task
    task : str            # the task

    @field_validator('userId')
    def validate_objectId(cls, user):
        try:
            ObjectId(str(user))
            return user
        except:
            raise ValueError('Invalid userId')

class GetUserTask(BaseModel):
    userId: str
    page: int = Field(default=1, gt=0)
    limit: int = Field(default=10, gt=0)

    @field_validator('userId')
    def validate_objectId(cls, user):
        try:
            ObjectId(str(user))
            return user
        except:
            raise ValueError('Invalid userId')
