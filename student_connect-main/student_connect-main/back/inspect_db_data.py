from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

print("=== TEMPLATES ===")
for t in db["templates"].find():
    print(f"Type: {t['type']}")
    print(f"Content (first 100 chars): {t['content'][:100]}...")
    print(f"Variables: {t.get('variables', [])}")
    print("-" * 20)

print("\n=== OUTPASSES (Last 3) ===")
for o in db["outpasses"].find().sort("created_at", -1).limit(3):
    print(f"ID: {o['_id']}")
    print(f"Student: {o.get('student_name')}")
    print(f"Status: {o.get('status')}")
    print(f"Document present: {'document' in o}")
    if 'document' in o:
        print(f"Document (first 100 chars): {o['document'][:100]}...")
    print("-" * 20)
