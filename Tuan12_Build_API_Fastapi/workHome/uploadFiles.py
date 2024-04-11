from fastapi import FastAPI,UploadFile,File
import shutil #copy file

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        import os
        if not os.path.exists("files"):
            os.makedirs("files")

        file_location = f"files/{file.filename}"
        with open(file_location, "wb+") as file_object: #mở 1 file cho phép write dưới dạng binary, đọc và ghi cùng lúc gán cho biến file_object
            shutil.copyfileobj(file.file, file_object)#sao chép nội dung file tải lên vào file mới mở
        return {"message": f"{file.filename} has been uploaded"}
    except Exception as e:
        return {"error": str(e)}