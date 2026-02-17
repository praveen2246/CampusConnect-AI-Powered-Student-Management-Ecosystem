from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
chat_collection = db["conversations"]
users_collection = db["users"]

def seed_admin():
    from werkzeug.security import generate_password_hash
    if not users_collection.find_one({"email": "admin@admin.com"}):
        hashed_pw = generate_password_hash("Admin")
        users_collection.insert_one({
            "name": "Admin",
            "email": "admin@admin.com",
            "password": hashed_pw,
            "role": "admin"
        })
        print("Admin user seeded: admin@admin.com / Admin")

    