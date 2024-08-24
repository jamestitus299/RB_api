from pydantic import BaseModel

class BaseResponse(BaseModel):
    msg: str

class LoginResponse(BaseModel):
    user: str
    access_token : str

class ErrorResponse(BaseModel):
    error : str