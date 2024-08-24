from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    name: str
    email: EmailStr  # primary key (also the id generated in the database)
    password: str

# The userType for a normal user is 0, for an admin user it is 1
class CreateAdminUser(BaseModel):
    name: str
    email: EmailStr  # primary key (also the id generated in the database)
    password: str
    secretKey: str   # to validate if the user is allowed to create an admin

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserId(BaseModel):
    userId: str
