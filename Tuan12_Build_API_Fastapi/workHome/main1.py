from typing import List
from fastapi import FastAPI, File, UploadFile
app = FastAPI()
@app.put("/example_type/")
def process_items(items: List[int]):
    response = 0
    for item in items:
        response += item
    return response

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    return {"Filename": file.filename, "Content": file.content_type}
