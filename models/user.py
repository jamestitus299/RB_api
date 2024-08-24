from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    name: str
    email: EmailStr  # primary key (also the id generated in the database)
    password: str
    userType : int | None = None # 1 is admin, 0 is general user

class CreateAdminUser(BaseModel):
    name: str
    email: EmailStr  # primary key (also the id generated in the database)
    password: str
    secretKey: str   # to validate if the user is allowed to create an admin
    userType : int | None = None # 1 is admin, 0 is general user

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserId(BaseModel):
    userId: str
