from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import *
from tortoise import models
import asyncmy as mysql
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_NAME=os.getenv("DATABASE_NAME")
HOST=os.getenv("HOST")
PORT=os.getenv("PORT")
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
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

@app.get('/')
def index():
    return {"Message":"Hello Minh dev dep trai ^^!"}

