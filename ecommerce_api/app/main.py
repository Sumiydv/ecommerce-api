import uvicorn
from fastapi import FastAPI
from app.products import router as products_router
from app.orders import router as orders_router

app = FastAPI(title="Ecommerce API")

# Include routers
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
