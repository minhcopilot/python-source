from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def hello():
    return {"title": "Hello Minh dev :)"}