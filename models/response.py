from typing import List
from pydantic import BaseModel

class BaseResponse(BaseModel):
    msg: str                # success msg

class LoginResponse(BaseModel):
    user: str               # user_id from database (_id)
    access_token : str      # JWT token

class ErrorResponse(BaseModel):
    error : str             # error msg

class TaskCreatedResponse(BaseModel):
    task : str              # the id of the created Task

class UserTaskResponse(BaseModel):
    tasks : List[str]       # list of tasks

class AdminTaskResponse(BaseModel):
    tasks : List[dict]      # list of dict of {task: user_info}

class NoteCreatedResponse(BaseModel):
    note : str              # the id of the created Note

class UserNoteResponse(BaseModel):
    notes : List[str]       # list of notes

class AdminNoteResponse(BaseModel):
    notes : List[dict]        # list of dict of {note: user_info} 