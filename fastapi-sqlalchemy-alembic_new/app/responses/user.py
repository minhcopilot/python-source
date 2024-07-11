from pydantic import EmailStr
from app.responses.base import BaseResponse
from typing import Union
from datetime import datetime
class UserResponse(BaseResponse):
    id:int
    name:str
    email:EmailStr
    is_active:bool
    created_at: Union[str, None, datetime] = None