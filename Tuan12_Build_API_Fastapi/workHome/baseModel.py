import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import numpy as np
from typing import List
import cv2

app = FastAPI()

class Response(BaseModel):
  filename: str
  contenttype: str
  image_shape: List[int]

@app.post('/upload/', response_model=Response)
async def prediction_route(file: UploadFile = File(...)):
    contents = await file.read()
    jpg_as_np = np.frombuffer(contents, dtype=np.uint8)
    input_image = cv2.imdecode(jpg_as_np, 0)

    return {
      'filename': file.filename,
      'contenttype': file.content_type,
      'image_shape': list(input_image.shape)
    }


