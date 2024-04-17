from passlib.context import CryptContext
import jwt
from dotenv import dotenv_values
from models import User
from fastapi import status
from fastapi.exceptions import HTTPException

config_cred = dotenv_values(".env")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_hashed_password(password):
    return password_context.hash(password)

async def very_token(token:str):
    try:
        payload = jwt.decode(token,config_cred.get("SECRET_KEY"),algorithms=["HS256"])
        user = await User.get(id=payload.get("id"))
    except:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
            headers={"WWW-Authenticate":"Bearer"} 
        )
    return user