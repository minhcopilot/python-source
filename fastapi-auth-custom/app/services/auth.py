from app.models.user import User
from fastapi.exceptions import HTTPException
from app.config.security import verify_password,create_access_token,create_refresh_token,get_token_payload,hash_password
from app.config.settings import get_settings
from datetime import timedelta
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from datetime import datetime 
settings=get_settings()

async def register(data,db):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
            raise HTTPException(status_code=400, detail={
                "status": 400,
                "message": "Email already exists"
            })
    new_user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=hash_password(data.password),
        is_active=False,
        is_verified=False,
        registered_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    payload = {
        "id":new_user.id,
        "email":new_user.email,
        "first_name":new_user.first_name,
        "last_name":new_user.last_name,
    }
    access_token_expires = timedelta(days=settings.JWT_TOKEN_EXPIRE)
    token=await create_access_token(payload,expires_delta=access_token_expires)
    refresh_token_expires = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE)
    refresh_token= await create_refresh_token(payload,expires_delta=refresh_token_expires)
    user_response = UserResponse.from_orm(new_user)
    return TokenResponse(token=token,refresh_token=refresh_token,token_type="bearer",data={
        "message":"Register successfully",
        "user":user_response.dict()
    })

async def login(data,db):
    user = db.query(User).filter(User.email == data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email is not registered with us.",headers={"WWW-Authenticate":"Bearer"})
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.",headers={"WWW-Authenticate":"Bearer"}) 
    payload = {
        "id":user.id,
        "email":user.email,
        "first_name":user.first_name,
        "last_name":user.last_name,
    }
    # _verify_user_access(user=user)
    access_token_expires = timedelta(days=settings.JWT_TOKEN_EXPIRE)
    token=await create_access_token(payload,expires_delta=access_token_expires)
    refresh_token_expires = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE)
    refresh_token= await create_refresh_token(payload,expires_delta=refresh_token_expires)
    
    user_response = UserResponse.from_orm(user)
    return TokenResponse(token=token,refresh_token=refresh_token,token_type="bearer",data={
        "message":"Login successfully",
        "user":user_response.dict()
    })

async def get_refresh_token(refresh_token,db):
    payload = get_token_payload(refresh_token)
    user_id = payload.get("id",None)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid refresh token",headers={"WWW-Authenticate":"Bearer"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid refresh token",headers={"WWW-Authenticate":"Bearer"})
    return await _get_user_token(user, refresh_token=refresh_token)
   
async def _get_user_token(user:User,refresh_token=None):
    payload = {
        "id":user.id,
        "email":user.email,
        "first_name":user.first_name,
        "last_name":user.last_name,
    }
    access_token_expires = timedelta(days=settings.JWT_TOKEN_EXPIRE)
    token=await create_access_token(payload,expires_delta=access_token_expires)
    if not refresh_token:
        refresh_token_expires = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE)
        refresh_token= await create_refresh_token(payload,expires_delta=refresh_token_expires)
    user_response = UserResponse.from_orm(user)
    return TokenResponse(token=token,refresh_token=refresh_token,token_type="bearer",data={
        "message":"Refresh token successfully",
        "user":user_response.dict()
    })

def _verify_user_access(user:User):
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Your account is not verified. Please check your email inbox to verify your account.")
    