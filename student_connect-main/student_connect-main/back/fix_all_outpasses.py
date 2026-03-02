from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson import ObjectId
import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
outpass_collection = db["outpasses"]
templates_collection = db["templates"]

# Fetch all approved outpasses
outpasses = list(outpass_collection.find({"status": "APPROVED"}))

if not outpasses:
    print("No approved outpasses found.")
    exit()

print(f"Found {len(outpasses)} approved outpasses to fix.")

for outpass in outpasses:
    print(f"Fixing outpass: {outpass['_id']} for {outpass.get('student_name')}")
    
    # Fetch the correct template
    cert_type = outpass.get("type", "outpass")
    tmpl = templates_collection.find_one({"type": cert_type})
    
    if not tmpl:
        print(f"Template not found for type: {cert_type}. Using fallback.")
        tmpl_content = """
        <div style="text-align: center; font-family: Arial, sans-serif;">
            <h1>Kamaraj College of Engineering and Technology</h1>
            <hr/>
            <h2>Outpass</h2>
            <p>Name: {student_name}</p>
            <p>Reason: {reason}</p>
        </div>
        """
    else:
        tmpl_content = tmpl["content"]
        
    student_id = outpass.get("student_id")
    # Fetch profile data for replacement
    profile_data = db["profile"].find_one({"user_id": student_id}) or {}
    
    # Prepare data for replacement
    replace_map = {
        "student_name": outpass.get("student_name") or profile_data.get("Name") or "Student",
        "date_from": outpass.get("date_from") or "N/A",
        "date_to": outpass.get("date_to") or "N/A",
        "reason": outpass.get("reason") or "N/A",
        "roll_no": profile_data.get("Roll No.") or "N/A",
        "department": outpass.get("extra_variables", {}).get("department") or profile_data.get("Department") or "N/A",
        "class": outpass.get("extra_variables", {}).get("class") or profile_data.get("Class") or "N/A",
        "gender": profile_data.get("Gender") or "N/A",
        "contact": profile_data.get("Father Mobile No.") or "N/A",
        "created_at": outpass.get("created_at").strftime("%Y-%m-%d %H:%M:%S") if outpass.get("created_at") else "N/A"
    }
    
    # Replace placeholders
    doc_content = tmpl_content
    for key, val in replace_map.items():
        placeholder = "{" + key + "}"
        doc_content = doc_content.replace(placeholder, str(val))
    
    # Update the outpass document
    outpass_collection.update_one(
        {"_id": outpass["_id"]}, 
        {"$set": {"document": doc_content}}
    )

print("Successfully regenerated ALL approved documents with new template!")
