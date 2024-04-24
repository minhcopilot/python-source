#Tạo môi trường ảo với các gói lib
python -m venv venv

#Chạy môi trường ảo  
venv\Scripts\activate

#Tạo migration mới
alembic revision --autogenerate -m "Mô tả migration"

#Áp dụng migration
alembic upgrade head

#chạy app
uvicorn app.main:app --reload

