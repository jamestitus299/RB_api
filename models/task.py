from pydantic import BaseModel, EmailStr

class Task(BaseModel):
    user: str           # user who create the task
    task : str          # the task

class GetUserTask(BaseModel):
    userId: str
    page : int | None = None
    limit: int | None = None 
