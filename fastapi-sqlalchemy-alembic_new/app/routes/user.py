from fastapi import APIRouter,status,Depends,BackgroundTasks
from requests import Session
from fastapi.responses import JSONResponse
from app.config.database import get_session
from app.responses.user import UserResponse
from app.schemas.user import RegisterUserRequest,VerifyUserRequest
from app.services import user
user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)

@user_router.post("",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def create_user(data: RegisterUserRequest, session: Session = Depends(get_session)):
    return await user.create_user_account(data,session)

@user_router.post("/verify",status_code=status.HTTP_200_OK)
async def verify_user_account(data:VerifyUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    await user.activate_user_account(data,background_tasks,session)
    return JSONResponse({
        "status":200,
        "message": "User verified successfully"
    })