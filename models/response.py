from typing import List
from pydantic import BaseModel

class BaseResponse(BaseModel):
    msg: str

class LoginResponse(BaseModel):
    user: str
    access_token : str

class ErrorResponse(BaseModel):
    error : str

class TaskCreatedResponse(BaseModel):
    task : str      # the id of the created Task


class UserTaskResponse(BaseModel):
    tasks : List[str]

class AdminTaskResponse(BaseModel):
    tasks : List[dict]

class NoteCreatedResponse(BaseModel):
    note : str      # the id of the created Note

class UserNoteResponse(BaseModel):
    notes : List[str]

class AdminNoteResponse(BaseModel):
    notes : List[dict]