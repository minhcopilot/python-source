from app.models.user import User
from app.config.security import hash_password,is_password_strong_enough,verify_password
from fastapi import HTTPException
from app.utils.email_context import FORGOT_PASSWORD, USER_VERIFY_ACCOUNT
import logging
from app.services.email import send_account_activation_confirmation_email
async def create_user_account(data,session):
    user_exists = session.query(User).filter(User.email == data.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already exists")
    if not is_password_strong_enough:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
    user = User()
    user.name = data.name
    user.email = data.email
    user.password = hash_password(data.password)
    user.is_active = False
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

async def activate_user_account(data,background_tasks,session):
    user = session.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.token = user.get_context_string(context=USER_VERIFY_ACCOUNT)
    try:
        token_valid = verify_password(user.token, data.token)
    except Exception as verify_exec:
        logging.exception(verify_exec)
        token_valid = False
    if not token_valid:
        raise HTTPException(status_code=400, detail="This link either expired or not valid")
    user.is_active = True
    user.verified_at = datetime.utcnow()
    user.update_at = datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)
    await send_account_activation_confirmation_email(user, background_tasks)
    return user