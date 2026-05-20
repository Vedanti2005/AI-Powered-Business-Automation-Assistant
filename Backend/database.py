import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import certifi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "codenixia_db")

client: AsyncIOMotorClient = None
db = None


async def connect_db():
    global client, db
    # Use certifi's CA bundle to ensure TLS handshakes work on Windows
    # This is especially necessary when connecting to MongoDB Atlas.
    client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client[DB_NAME]

    # Create indexes
    await db.leads.create_index("email", unique=True)
    await db.chat_sessions.create_index("session_id")
    await db.automation_logs.create_index("created_at")

    print(f"✅ Connected to MongoDB: {DB_NAME}")


async def close_db():
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed.")


def get_db():
    return db
