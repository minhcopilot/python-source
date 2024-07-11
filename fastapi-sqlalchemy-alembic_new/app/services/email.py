from fastapi import BackgroundTasks
from app.config.settings import get_settings
from app.models.user import User
from app.config.email import send_email

settings = get_settings()

async def send_account_activation_confirmation_email(user: User, background_tasks: BackgroundTasks):
    data={
        "app_name":settings.APP_NAME,
        "name":user.name,
        "login_url":f"{settings.FRONTEND_HOST}",
    }
    subject = "Welcome - {settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/account_verification_confirmation.html",
        context=data,
        background_tasks=background_tasks
    )
    