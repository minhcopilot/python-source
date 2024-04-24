from fastapi import APIRouter,status,Depends,Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.auth import login,get_refresh_token,register
from app.schemas.user import CreateUserRequest
router=APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404:{"description":"Not found"}}
)

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_user(data:CreateUserRequest,db:Session = Depends(get_db)):
    return await register(data=data,db=db)
    
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await login(data=data, db=db)

@router.post("/refresh-token",status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token:str=Header(),db:Session=Depends(get_db)):
    return await get_refresh_token(refresh_token=refresh_token, db=db)