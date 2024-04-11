from fastapi import FastAPI, File, UploadFile #lib xử lý file
from fastapi import Depends, HTTPException,status #lib lỗi và status code
from fastapi.security import HTTPBasic,HTTPBasicCredentials #lib xác thực basic
import secrets #so sánh chuỗi

app = FastAPI()
security = HTTPBasic() # khởi tạo đối HTTPBasic xác thực cơ bản HTTP
AUTH_USERNAME ="minhdev"
AUTH_PASSWORD ="123456"

def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username =secrets.compare_digest(credentials.username, AUTH_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, AUTH_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
@app.post("/upload")
async def upload(file: UploadFile =File(...),auth=Depends(verify_user)):
    contents = await file.read()
    return {"Filename": file.filename, "Content": file.content_type}

