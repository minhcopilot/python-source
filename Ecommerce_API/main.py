from fastapi import FastAPI,Request,status
from tortoise.contrib.fastapi import register_tortoise
from models import *
from tortoise import models
import asyncmy as mysql
from dotenv import dotenv_values
import os
from authentication import (get_hashed_password, very_token)
from fastapi.exceptions import HTTPException
#signals
from tortoise.signals import post_save
from typing import List, Optional,Type
from tortoise import BaseDBAsyncClient
from emails import *
#response class
from fastapi.responses import HTMLResponse

#templates
from fastapi.templating import Jinja2Templates


config_cred = dotenv_values(".env")
DATABASE_NAME=config_cred.get("DATABASE_NAME")
HOST=config_cred.get("HOST")
PORT=config_cred.get("PORT")
USER=config_cred.get("USER")
PASSWORD=config_cred.get("PASSWORD")
db_url = f"mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"

app=FastAPI()
#Register tortoise to mysql
register_tortoise(
    app,
    db_url=db_url,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

#Hàm callback được gọi khi tạo đối tượng User
@post_save(User)
async def create_business(
    sender:"Type[User]",
    instance:User,
    created:bool,
    using_db:"Optional[BaseDBAsyncClient]",
    update_fields:List[str]
) -> None:
    #nếu mà User được tạo nó sẽ tự động Tạo 1 đối tượng Business với business_name = instance.username
    if created:
        business_obj = await Business.create(
            business_name =instance.username,owner = instance
        )
        await business_pydantic.from_tortoise_orm(business_obj)
        #send email to user
        await send_email(email=instance.email,instance=instance)
        
@app.post('/registration')
async def user_registration(user:user_pydanticIn):
    try:
        user_info= user.dict(exclude_unset=True)
        user_info["password"]=get_hashed_password(user_info["password"])
        #tạo 1 đối tượng bằng ORM, **user_info truyền cặp key-value từ dict user_info
        user_obj = await User.create(**user_info)
        new_user = await user_pydanticOut.from_tortoise_orm(user_obj)
        return{
            "status":200,
            "payload":{
                "data":new_user,
                "message":"User created successfully"
            }
        }
    except Exception as e:
        return {"error":str(e)}

templates = Jinja2Templates(directory="templates")
@app.get('/verification',response_class=HTMLResponse)
async def email_verification(request:Request,token:str):
    user = await very_token(token)
    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse("verification.html",{"request":request,"username":user.username})
    raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
            headers={"WWW-Authenticate":"Bearer"} 
        )
@app.get('/')
def index():
    return {"Message":"Hello Minh dev dep trai ^^!"}

