from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

print("=== STUDENT PROFILES ===")
profiles = list(db["profile"].find())
if not profiles:
    print("No profiles found.")
else:
    for p in profiles:
        print(f"User: {p.get('user_id')}")
        print(f"Name: {p.get('Name')}")
        print(f"Roll No: {p.get('Roll No.')}")
        print(f"Dept: {p.get('Department')}")
        print("-" * 20)

print("\n=== RECENT OUTPASSES DATA ===")
for o in db["outpasses"].find().sort("created_at", -1).limit(5):
    print(f"ID: {o['_id']}")
    print(f"Doc ID extracted: {o.get('document', '')[o.get('document', '').find('Document ID:'):o.get('document', '').find('|') + 50]}")
    print("-" * 20)
