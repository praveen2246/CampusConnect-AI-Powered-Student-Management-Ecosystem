from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

outpass = db["outpasses"].find_one(sort=[("created_at", -1)])
if outpass:
    print("--- ID ---")
    print(outpass["_id"])
    print("--- Status ---")
    print(outpass["status"])
    print("--- Document Content (HTML) ---")
    print(outpass.get("document", "No Document Field"))
else:
    print("No outpass found.")
