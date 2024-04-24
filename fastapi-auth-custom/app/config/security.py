from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.config.settings import get_settings
from datetime import datetime, timedelta
from jose import jwt,JWTError
from fastapi.exceptions import HTTPException
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from fastapi import Depends
from fastapi.responses import JSONResponse
from app.config.database import get_db
from app.models.user import User
settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_access_token(data, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def create_refresh_token(data,expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        error={
            "status":401,
            "detail":"Invalid token"
        }
        return JSONResponse(content=error,status_code=401)
    return payload

def get_current_user(token: str = Depends(oauth2_scheme), db= None):
    payload = get_token_payload(token)
    if not payload or not isinstance(payload, dict):
        error={
            "status":401,
            "detail":"Invalid token"
            }
        return JSONResponse(content=error,status_code=401)
    user_id = payload.get("id", None)
    if not user_id:
        error={
            "status":404,
            "detail":"User not found"
            }
        return JSONResponse(content=error,status_code=404)
    if not db:
        db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    return user

def is_token_valid(token: str) -> bool:
    try:
        payload = get_token_payload(token)
        if not payload or type(payload) is not dict:
            return False
        user_id = payload.get("id", None)
        if not user_id:
            return False
        return True
    except HTTPException:
        return False
    
class JWTAuth:
    async def authenticate(self,conn):
        guest =AuthCredentials(["unauthenticated"]),UnauthenticatedUser()
        if "authorization" not in conn.headers:
            return guest
        token = conn.headers.get("Authorization").split(' ')[1]
        if not token:
            return guest
        user = is_token_valid(token=token)
        if not user:
            return guest
        return AuthCredentials("authenticated"), None