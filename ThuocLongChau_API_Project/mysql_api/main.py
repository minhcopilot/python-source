from fastapi import FastAPI
from database import sync_products

app = FastAPI()

@app.get('/')
def home():
    return {"title": "Hello Minh dev :)"}
@app.get("/get_products_longchau")
def sync_products_endpoint(keyword: str = ''):
    return sync_products(keyword)

