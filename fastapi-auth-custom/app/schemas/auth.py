from pydantic import BaseModel

class TokenResponse(BaseModel):
    token: str
    refresh_token: str
    token_type: str
    data:object
    class Config:
        from_attributes = True
        
class RegisterResponse(BaseModel):
    token: str
    refresh_token: str
    token_type: str
    data:object
    class Config:
        from_attributes = True