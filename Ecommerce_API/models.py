import pydantic
from tortoise import Model, fields
from pydantic import BaseModel
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
class User(Model):
    id = fields.IntField(pk=True,index=True)
    username = fields.CharField(max_length=255,null=False)
    email =fields.CharField(max_length=255,null=False,unique=True)
    password = fields.CharField(max_length=100,null=False)
    is_verified = fields.BooleanField(default=False)
    join_data = fields.DatetimeField(default=datetime.now)

class Business(Model):
    id = fields.IntField(pk=True,index=True)
    business_name = fields.CharField(max_length=255,null=False)
    city = fields.CharField(max_length=255,null=False,default="Unspecified")
    region =fields.CharField(max_length=255,null=False,default="Unspecified")
    business_description = fields.CharField(max_length=255,null=False)
    logo = fields.CharField(max_length=255,null=False,default="default.jpg")
    owner = fields.ForeignKeyField("models.User",related_name="business")#PK 1 User có nhiều Business
    
class Category(Model):
    id = fields.IntField(pk=True,index=True)
    name = fields.CharField(max_length=255,null=False)
class Product(Model):
    id = fields.IntField(pk=True,index=True)
    name = fields.CharField(max_length=255,null=False,index=True)
    original_price = fields.DecimalField(max_digits=10,decimal_places=2)
    new_price = fields.DecimalField(max_digits=10,decimal_places=2)
    percentage_discount = fields.IntField()
    offer_expiration_data = fields.DateField(default=datetime.date(datetime.now()))
    product_image = fields.CharField(max_length=255,null=False,default="productDefault.jpg")
    business = fields.ForeignKeyField("models.Business",related_name="products")#PK 1 Business có nhiều Product
    category = fields.ForeignKeyField("models.Category",related_name="products")#PK 1 Category có nhiều Product
    
#create các class Pydantic data object, data input, data output
user_pydantic = pydantic_model_creator(User, name="User",exclude=("is_verified",))
user_pydanticIn = pydantic_model_creator(User, name="UserIn",exclude_readonly=True)#exclude_readonly loại bỏ các trường chỉ đọc được để cập nhập được dữ liệu
user_pydanticOut = pydantic_model_creator(User, name="UserOut",exclude=("password",))#Xuất ra User loại bỏ trường Password

business_pydantic = pydantic_model_creator(Business, name="Business")
business_pydanticIn = pydantic_model_creator(Business, name="BusinessIn",exclude_readonly=True)

product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticIn = pydantic_model_creator(Product, name="ProductIn",exclude=("id","percentage_discount"))#Exclude id, percentage_discount
