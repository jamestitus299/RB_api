from pydantic import BaseModel, EmailStr, Field

class Task(BaseModel):
    user: str           # user who create the task
    task : str          # the task

class GetUserTask(BaseModel):
    userId: str
    page: int = Field(default=1, gt=0)
    limit: int = Field(default=10, gt=0)
