from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    db = client[MONGO_DB_NAME]
    server_info = client.server_info()
    print(f"Successfully connected to MongoDB! Server version: {server_info.get('version')}")
    print(f"Database: {MONGO_DB_NAME}")
    print(f"Collections: {db.list_collection_names()}")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
