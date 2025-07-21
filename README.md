# 🛒 Ecommerce API with FastAPI + MongoDB

This is a simple backend ecommerce API built using **FastAPI** and **MongoDB** (via Motor)

## 🚀 Features

- Create and list products
- Create orders and view orders by user
- Filter/search products by name and size
- Pagination support (`limit`, `offset`)
- MongoDB Atlas for storage
- Deployed on Replit

---

## 🔌 API Endpoints

### 📦 Products

#### ➕ Create Product
- `POST /products`
```json
{
  "name": "T-shirt",
  "size": "large",
  "price": 499
}
