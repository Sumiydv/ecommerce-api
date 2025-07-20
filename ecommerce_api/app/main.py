import uvicorn
from fastapi import FastAPI
from app.products import router as products_router
from app.orders import router as orders_router
from app.auth import router as auth_router

app = FastAPI(title="Ecommerce API", description="A comprehensive ecommerce API with authentication, categories, and advanced search")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Ecommerce API", 
        "docs": "/docs",
        "features": [
            "User authentication (register/login)",
            "Product categories and search",
            "Advanced filtering (price, stock, category)",
            "Order management"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running properly"}

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
