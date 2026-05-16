import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "ai_chat_db")

class Database:
    client: AsyncIOMotorClient = None
    
db_instance = Database()

def get_database():
    return db_instance.client[MONGODB_DB_NAME]

def get_collection(name: str):
    return get_database().get_collection(name)

async def connect_db():
    db_instance.client = AsyncIOMotorClient(MONGODB_URL, tlsCAFile=certifi.where())

async def close_db():
    if db_instance.client is not None:
        db_instance.client.close()
