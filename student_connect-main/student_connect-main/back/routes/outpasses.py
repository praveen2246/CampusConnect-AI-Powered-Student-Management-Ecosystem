from flask import Blueprint, request, jsonify
from db import db
import datetime
import jwt
import os

outpass_bp = Blueprint('outpass', __name__)
outpass_collection = db["outpasses"]
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

def verify_token(req):
    token = req.headers.get("Authorization")
    if not token: return None
    try:
        if token.startswith("Bearer "): token = token.split(" ")[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except:
        return None

@outpass_bp.route("/request", methods=["POST"])
def request_outpass():
    user = verify_token(request)
    if not user: return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    new_outpass = {
        "student_id": user["user_id"],
        # In a real app we'd fetch name from DB, but for now expect it or use ID
        "student_name": data.get("student_name", "Student"), 
        "reason": data["reason"],
        "date_from": data["date_from"],
        "date_to": data["date_to"],
        "status": "PENDING",
        "created_at": datetime.datetime.utcnow()
    }
    outpass_collection.insert_one(new_outpass)
    return jsonify({"message": "Outpass requested successfully"})

@outpass_bp.route("/my", methods=["GET"])
def my_outpasses():
    user = verify_token(request)
    if not user: return jsonify({"error": "Unauthorized"}), 401
    
    outpasses = list(outpass_collection.find({"student_id": user["user_id"]}).sort("created_at", -1))
    for o in outpasses:
        o["_id"] = str(o["_id"])
    return jsonify(outpasses)
