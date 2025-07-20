from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.db import orders_collection
from app.models import OrderModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/", status_code=201)
async def create_order(order: OrderModel):
    order = jsonable_encoder(order)
    new_order = await orders_collection.insert_one(order)
    created_order = await orders_collection.find_one({"_id": new_order.inserted_id})
    return JSONResponse(status_code=201, content=created_order)

@router.get("/{user_id}")
async def list_orders(
    user_id: str,
    limit: int = 10,
    offset: int = 0
):
    query = {"user_id": user_id}
    orders_cursor = orders_collection.find(query).skip(offset).limit(limit)
    orders = await orders_cursor.to_list(length=limit)
    return orders
