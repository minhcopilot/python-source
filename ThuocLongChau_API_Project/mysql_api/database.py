import mysql.connector
import requests
from pydantic import BaseModel
from dotenv import dotenv_values
class Category(BaseModel):
    id: int
    name: str
    parent_name: str
    slug: str
    level: int
    is_active: bool

class Product(BaseModel):
    id: int
    sku: str
    name: str
    webName: str
    image: str
    category_id: int
    price: float
    slug: str
    ingredients: str
    dosage_form: str
    brand: str
    display_code: int
    is_active: bool
    is_publish: bool
    search_scoring: float
    product_ranking: float
    specification: str

config_cred = dotenv_values(".env")

DATABASE_NAME=config_cred.get("DATABASE_NAME")
HOST=config_cred.get("HOST")
PORT=config_cred.get("PORT")
USER=config_cred.get("USER")
PASSWORD=config_cred.get("PASSWORD")

db = mysql.connector.connect(
    host=HOST,
    user=USER,
    port=PORT,
    password=PASSWORD,
    database=DATABASE_NAME
)
cursor = db.cursor()

def sync_products(keyword: str = ''):
    try:
        url="https://nhathuoclongchau.com.vn/_next/data/whzzTXfLkIB5rlvjBO5as/tim-kiem.json?s="
        response = requests.get(url+keyword)
        data = response.json() #parse chuỗi JSON thành một dict Python.
        

        for product in data["pageProps"]["initProducts"]["products"]:
            # Kiểm tra xem danh mục đã có chưa nếu có thì lấy id còn ngược lại thì tạo mới
            category_sql = "SELECT id FROM categories WHERE slug = %s"
            cursor.execute(category_sql, (product["category"][0]["slug"],))
            
            category = cursor.fetchone()
            if category:
                category_id = category[0]
            else:
                category_sql = "INSERT INTO categories (name, parent_name, slug, level, is_active) VALUES (%s, %s, %s, %s, %s)"
                category_values = (
                    product["category"][0]["name"],
                    product["category"][0]["parentName"],
                    product["category"][0]["slug"],
                    product["category"][0]["level"],
                    product["category"][0]["isActive"]
                )
                cursor.execute(category_sql, category_values)
                # lấy id của bản ghi vừa insert bằng cursor.lastrowid và gán vào category_id
                category_id = cursor.lastrowid

            product_sql = "INSERT INTO products (sku, name, webName, image, category_id, price, slug, ingredients, dosage_form, brand, display_code, is_active, is_publish, search_scoring, product_ranking, specification) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            product_values = (
                product["sku"],
                product["name"],
                product["webName"],
                product["image"],
                category_id,
                product["price"]["price"],
                product["slug"],
                product["ingredients"],
                product["dosageForm"],
                product["brand"],
                product["displayCode"],
                product["isActive"],
                product["isPublish"],
                product["searchScoring"],
                product["productRanking"],
                product["specification"]
            )
            cursor.execute(product_sql, product_values)

        db.commit()
        return {"message": "Dữ liệu đã được lưu vào MySQL thành công."}
    except Exception as e:
        return {"error": str(e)}