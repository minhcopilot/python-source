from fastapi import FastAPI,File,UploadFile

app=FastAPI()

# @app.post("/upload")
# async def upload(file:UploadFile=File(...)):
#     content = await file.read()
#     return {"filename":file.filename,"content":content.decode("utf-8"), "type": file.content_type,"size": file.size}

@app.post("/upload")
async def upload(file:UploadFile=File(...)):
    file_location = f"upload/{file.filename}"
    with open(file_location, "wb+") as file_object:
        binary = b"\x48\x65\x6c\x6c\x6f"
        file_object.write(binary)
    return { "message": f"{file.filename} has been uploaded"}