from fastapi import (BackgroundTasks, UploadFile,File,Form,Depends,HTTPException,status)
from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from dotenv import dotenv_values
from pydantic import BaseModel,EmailStr
from typing import List
from models import User
import jwt
config_cred = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config_cred.get('MAIL_USERNAME'),
    MAIL_PASSWORD=config_cred.get('EMAIL_APP_PASSWORD'),
    MAIL_FROM=config_cred.get('MAIL_USERNAME'),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)

class EmailSchema(BaseModel):
    email:List[EmailStr]
    
    
async def send_email(email:EmailSchema, instance:User):
    try:
        token_data={
            "id":instance.id,
            "email":instance.email,
            "username":instance.username
        }
        token = jwt.encode(token_data, config_cred.get('SECRET_KEY'), algorithm="HS256")
        template =f"""
           <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div style="padding: 1rem; margin-top: 5vh; margin-bottom: 5vh">
      <h3>Xác thực tài khoản</h3>

      <p>
        Cảm ơn bạn đã đăng ký tài khoản của website chúng tôi! Hãy nhấn vào nút
        phía dưới để xác thực tài khoản
      </p>
      <div style="margin-top: 2rem;">
        <a
        style="
          margin-top: 1rem;
          padding: 1rem;
          border-radius: 0.5rem;
          font-size: 1.2rem;
          text-decoration: none;
          background-color: #0275d8;
          color: white;
        "
        href="http://localhost:8000/verification/?token={token}"
        >Xác thực Email</a
      </div>
    </div>
  </body>
</html>

        """
        message =MessageSchema(
            subject="Xác thực tài khoản",
            recipients=[email],
            body=template,
            subtype="html"
        )
        fm=FastMail(conf)
        await fm.send_message(message=message)
    except Exception as e:
        print("error:",e)
