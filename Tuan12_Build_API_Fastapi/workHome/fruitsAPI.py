from fastapi import FastAPI
import pandas as pd

app = FastAPI()
data = pd.read_csv('fruits.csv')

@app.get("/fruit/{name}")
def get_fruit_price(name: str):
    try:
        price = data[data['fruit'] == name.lower()]
        fruit_price = price.to_dict('records')#chuyển dataframe về 1 mảng các object
        if fruit_price:
            fruit_info = fruit_price[0]  # Lấy phần tử đầu tiên trong danh sách
            return {"fruit": name, "price": fruit_info["price"]}
        else:
            return {"error": "Fruit not found"}
    except Exception as e:
        return {"error": str(e)}