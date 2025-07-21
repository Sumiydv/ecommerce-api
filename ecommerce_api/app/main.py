import uvicorn
from fastapi import FastAPI
from ecommerce_api.products import router as products_router
from ecommerce_api.orders import router as orders_router

app = FastAPI(
    title="Ecommerce API",
    description="A comprehensive ecommerce API with product categories and advanced search"
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Ecommerce Backend",
        "endpoints": [
            "/health", "/products", "/products/{product_id}",
            "/products/search/", "/products/categories/", "/orders",
            "/orders/{user_id}"
        ],
        "documentation": "/docs",
        "health_check": "To check the health of the API, visit /health"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running properly"}


# Include routers
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])


if __name__ == "__main__":
    uvicorn.run("ecommerce_api.main:app", host="0.0.0.0", port=8000, reload=True)
