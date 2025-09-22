from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = getenv("MONGO_URI", "mongodb://localhost:27017")

_client: AsyncIOMotorClient | None = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        print("[DB] Initializing Mongo client...")
        _client = AsyncIOMotorClient(MONGO_URI)
        _db = _client["100xprojects"]
    return _db
