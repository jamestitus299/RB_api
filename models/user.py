from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    links: list[int] | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str