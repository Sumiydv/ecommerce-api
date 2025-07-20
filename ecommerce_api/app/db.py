import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

MONGODB_URL = os.getenv("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.ecommerce  # your database name

products_collection = database.get_collection("products")
orders_collection = database.get_collection("orders")
categories_collection = database.get_collection("categories")
users_collection = database.get_collection("users")
