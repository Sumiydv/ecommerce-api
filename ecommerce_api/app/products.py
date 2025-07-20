from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.db import products_collection
from app.models import ProductModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/", status_code=201)
async def create_product(product: ProductModel):
    product = jsonable_encoder(product)
    new_product = await products_collection.insert_one(product)
    created_product = await products_collection.find_one({"_id": new_product.inserted_id})
    return JSONResponse(status_code=201, content=created_product)

@router.get("/")
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes"] = size

    products_cursor = products_collection.find(query).skip(offset).limit(limit)
    products = await products_cursor.to_list(length=limit)
    return products
