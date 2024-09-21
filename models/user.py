from bson import ObjectId
from pydantic import BaseModel, EmailStr, field_validator

class CreateUser(BaseModel):
    name: str
    email: str  # primary key (also the id generated in the database)
    password: str

# The userType for a normal user is 0, for an admin user it is 1 (in the database)
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

    @field_validator('userId')
    def validate_objectId(cls, user):
        try:
            ObjectId(str(user))
            return user
        except:
            raise ValueError('Invalid userId')
