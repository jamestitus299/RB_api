from pydantic import BaseModel, EmailStr

class Task(BaseModel):
    user: str           # user who create the task
    task : str