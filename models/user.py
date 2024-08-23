from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    name: str
    email: EmailStr  # primary key and the id generated in the database
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str
