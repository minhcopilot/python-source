from pydantic import BaseModel,EmailStr
from typing import Optional

class CreateUserRequest(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    password:str
    
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None