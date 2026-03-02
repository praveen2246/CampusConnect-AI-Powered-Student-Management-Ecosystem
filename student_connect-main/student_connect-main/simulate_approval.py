import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="back/.env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

def approve_latest():
    outpass = db["outpasses"].find_one(sort=[("created_at", -1)])
    if not outpass:
        print("No outpass found")
        return
    
    outpass_id = str(outpass["_id"])
    print(f"Approving outpass ID: {outpass_id} for {outpass.get('student_name')}")
    
    url = f"http://localhost:8000/admin/outpasses/{outpass_id}"
    try:
        res = requests.put(url, json={"status": "APPROVED"})
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    approve_latest()
