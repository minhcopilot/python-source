from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Đường dẫn tới file CSV
CSV_FILE_PATH = "info.csv"

# Kiểm tra xem file CSV đã tồn tại chưa, nếu không thì tạo mới
try:
    pd.read_csv(CSV_FILE_PATH)
except FileNotFoundError:
    pd.DataFrame(columns=["CCCD", "Name", "Phone"]).to_csv(CSV_FILE_PATH, index=False)


# Model để validate dữ liệu đầu vào
class InfoInput(BaseModel):
    cccd: str
    name: str
    phone: str


# API để thêm thông tin vào file CSV
@app.post("/add-info/")
def add_info(info: InfoInput):
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        
        # Kiểm tra xem CCCD đã tồn tại trong DataFrame hay chưa
        condition = (df['CCCD'].astype(str).values == info.cccd) | (info.name in df['Name'].astype(str).values)
        if condition.any():
            raise HTTPException(status_code=400, detail="CCCD or Name already exists")

        new_row = {"CCCD": info.cccd, "Name": info.name, "Phone": info.phone}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE_PATH, index=False)
        return {"message": "Information added successfully"}
    except Exception as e:
        return {"error": str(e)}
    
#get info
@app.get('/get-info')
def get_info(name: str):
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        if name not in df['Name'].astype(str).values:
            raise HTTPException(status_code=404, detail="Name not found")
        else:
            return {"name": name, "info": df[df['Name'] == name].to_dict('records')[0]}
    except Exception as e:
        return {"error": str(e)}