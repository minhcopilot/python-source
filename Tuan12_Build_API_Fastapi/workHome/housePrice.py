from fastapi import FastAPI
import pandas as pd

app = FastAPI()

data = pd.read_csv('house-prices.csv')

@app.get("/houses")
def get_houses(min_price: int = 0, max_price: int = 1000000000, neighborhood: str = None):
    try:
        filtered_data = data[(data['Price'] >= min_price) & 
                            (data['Price'] <= max_price)]
        
        if neighborhood:
            filtered_data = filtered_data[filtered_data['Neighborhood'] == neighborhood]
        houses = filtered_data.to_dict('records')
        
        return houses
    except Exception as e:
        return {"error": str(e)}