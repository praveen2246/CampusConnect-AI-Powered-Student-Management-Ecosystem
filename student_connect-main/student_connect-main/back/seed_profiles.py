from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

users = list(db["users"].find())
print(f"Found {len(users)} users. Creating dummy profiles...")

for user in users:
    user_id = str(user["_id"])
    profile_exists = db["profile"].find_one({"user_id": user_id})
    
    if not profile_exists:
        dummy_profile = {
            "user_id": user_id,
            "Name": user.get("name", "Student"),
            "Roll No.": f"21CS{str(hash(user_id))[-3:]}",
            "Department": "Computer Science and Engineering",
            "Class": "III Year / VI Sem",
            "Gender": "Male",
            "Father Mobile No.": "9876543210"
        }
        db["profile"].insert_one(dummy_profile)
        print(f"Created profile for: {user.get('name')}")
    else:
        # Update existing profile if fields are missing
        db["profile"].update_one(
            {"user_id": user_id},
            {"$set": {
                "Roll No.": profile_exists.get("Roll No.") or f"21CS{str(hash(user_id))[-3:]}",
                "Department": profile_exists.get("Department") or "Computer Science and Engineering",
                "Class": profile_exists.get("Class") or "III Year / VI Sem"
            }}
        )
        print(f"Updated profile for: {user.get('name')}")

print("Profile seeding/update complete.")
