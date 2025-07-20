
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.db import products_collection, categories_collection
from app.models import ProductModel, CategoryModel
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
    name: Optional[str] = Query(None, description="Filter by product name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    size: Optional[str] = Query(None, description="Filter by available size"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    in_stock: Optional[bool] = Query(None, description="Filter by stock availability"),
    sort_by: Optional[str] = Query("name", description="Sort by: name, price, category"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    limit: int = Query(10, description="Number of products to return"),
    offset: int = Query(0, description="Number of products to skip")
):
    query = {}
    
    # Build query filters
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    if size:
        query["sizes"] = size
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        query["price"] = price_filter
    if in_stock is not None:
        if in_stock:
            query["stock_quantity"] = {"$gt": 0}
        else:
            query["stock_quantity"] = {"$lte": 0}

    # Build sort criteria
    sort_direction = 1 if sort_order == "asc" else -1
    sort_criteria = [(sort_by, sort_direction)]

    products_cursor = products_collection.find(query).sort(sort_criteria).skip(offset).limit(limit)
    products = await products_cursor.to_list(length=limit)
    
    # Get total count for pagination
    total_count = await products_collection.count_documents(query)
    
    return {
        "products": products,
        "total_count": total_count,
        "limit": limit,
        "offset": offset
    }

@router.get("/{product_id}")
async def get_product(product_id: str):
    from bson import ObjectId
    try:
        product = await products_collection.find_one({"_id": ObjectId(product_id)})
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID")

# Categories endpoints
@router.post("/categories/", status_code=201)
async def create_category(category: CategoryModel):
    category = jsonable_encoder(category)
    new_category = await categories_collection.insert_one(category)
    created_category = await categories_collection.find_one({"_id": new_category.inserted_id})
    return JSONResponse(status_code=201, content=created_category)

@router.get("/categories/")
async def list_categories():
    categories = await categories_collection.find().to_list(length=None)
    return categories

@router.get("/search/")
async def search_products(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(10, description="Number of products to return")
):
    query = {
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"category": {"$regex": q, "$options": "i"}}
        ]
    }
    
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    
    products_cursor = products_collection.find(query).limit(limit)
    products = await products_cursor.to_list(length=limit)
    return products
