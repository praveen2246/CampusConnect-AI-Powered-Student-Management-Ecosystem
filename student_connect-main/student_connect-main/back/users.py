from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
import jwt, datetime
import os
from dotenv import load_dotenv

load_dotenv()

users_bp = Blueprint('users', __name__)
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
JWT_EXPIRY_DAYS = int(os.getenv("JWT_EXPIRY_DAYS", 30))

users_collection = db["users"]

@users_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        if not data or "email" not in data or "password" not in data or "name" not in data:
            return jsonify({"error": "Missing required fields"}), 400
            
        if users_collection.find_one({"email": data["email"]}):
            return jsonify({"error": "Email already exists"}), 400
            
        hashed_pw = generate_password_hash(data["password"])
        users_collection.insert_one({
            "name": data["name"],
            "email": data["email"],
            "password": hashed_pw,
            "created_at": datetime.datetime.utcnow()
        })
        return jsonify({"message": "Signup successful"})
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({"error": "Internal server error during signup"}), 500

@users_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users_collection.find_one({"email": data["email"]})
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    
    token = jwt.encode({
        "user_id": str(user["_id"]),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=JWT_EXPIRY_DAYS)
    }, SECRET_KEY, algorithm="HS256")
    
    # Handle PyJWT version differences (v1 returns bytes, v2 returns str)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
        
    return jsonify({"token": token, "name": user["name"]})