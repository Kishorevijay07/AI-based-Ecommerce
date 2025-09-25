from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = "mongodb+srv://kishorevijay978_db_user:sq3kcxmI7sahPopO@ecommerce.sb0tnfi.mongodb.net/?retryWrites=true&w=majority&appName=Ecommerce"
# Create Mongo client
client = AsyncIOMotorClient(MONGO_URL)

# Choose database
db = client["ecommerce_db"]

async def connect_db():
    """Check MongoDB connection"""
    try:
        await db.command("ping")
        print("✅ MongoDB Atlas connection established")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

async def close_db():
    """Close MongoDB connection"""
    client.close()
    print("❌ MongoDB connection closed")
