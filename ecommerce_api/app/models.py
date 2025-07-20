from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Any
from bson import ObjectId
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler):
        from pydantic_core import core_schema
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class CategoryModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Electronics",
                "description": "Electronic devices and accessories"
            }
        }
    )
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None

class ProductModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Cool Shirt",
                "price": 499.99,
                "sizes": ["small", "medium", "large"],
                "category": "Clothing",
                "description": "A comfortable cotton shirt"
            }
        }
    )
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    price: float
    sizes: List[str]
    category: str
    description: Optional[str] = None
    stock_quantity: int = 0

class UserModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "password123",
                "name": "John Doe"
            }
        }
    )
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    password: str
    name: str
    created_at: datetime = Field(default_factory=datetime.now)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
    
    id: PyObjectId = Field(alias="_id")
    email: str
    name: str
    created_at: datetime

class OrderModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": "user123",
                "products": ["60d5f4e8c3d45678abcdef01"],
                "total_price": 499.99
            }
        }
    )
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    products: List[str]  # List of product IDs
    total_price: float
