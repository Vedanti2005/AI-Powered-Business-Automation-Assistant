import os, certifi
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")
print("Using URI host:", uri.split("@")[-1][:200])
try:
    client = MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=10000)
    print("Attempting server_info() ...")
    print(client.server_info())
except PyMongoError as e:
    print("Connection error:", repr(e))