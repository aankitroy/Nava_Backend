from pydantic import BaseModel
from pydantic import EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AdminCreateRequest(BaseModel):
    email: EmailStr
    password: str

class AdminDeleteRequest(BaseModel):
    email: EmailStr