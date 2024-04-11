from fastapi import FastAPI

app =FastAPI()

@app.get("/")
def index():
    return {"title": "Hello Minh dev :)"}

@app.get('/minus')
def minus_numbers(number1:int,number2:int):
    return {"result minus numbers": number1 - number2}

fruit_price ={
    'xoai':10,\
    'oi':15,\
    'kiwi':20
}
@app.get('/fruit')
def get_price(name:str):
    lookup_name = name.lower()
    if lookup_name in fruit_price:
        return {"fruit": lookup_name, "price": fruit_price[lookup_name]}