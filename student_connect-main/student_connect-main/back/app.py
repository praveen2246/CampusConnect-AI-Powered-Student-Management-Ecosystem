from flask import Flask, request, jsonify
from flask_cors import CORS
from db import chat_collection, db, seed_admin
from users import users_bp
from admin import admin_bp
from routes.outpasses import outpass_bp
import jwt
import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.register_blueprint(users_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(outpass_bp, url_prefix="/outpass")

# Seed admin user
seed_admin()

RASA_URL = os.getenv("RASA_URL", "http://localhost:5005/webhooks/rest/webhook")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
FLASK_PORT = int(os.getenv("FLASK_PORT", 8000))

profile_collection = db["profile"]

def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token missing"}), 401
        
        # Strip "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        token = token.strip()
            
        try:
            user_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401
        return f(user_data, *args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

@app.route("/chat", methods=["POST"])
@token_required
def chat(user_data):
    user_message = request.json.get("message")
    conversation_name = request.json.get("conversation_name")  # Get from frontend

    # Send message to Rasa with sender as user_id and pass token as event to set slot
    # We first send the message, then Rasa will have the tracker.
    # To set the slot initially, we could use the Rasa API or just rely on the sender_id.
    # Let's just use sender_id = user_id for now. 
    # To pass the token, we can use metadata or include it in the sender field if we wanted to be hacky, 
    # but let's stick to standard sender_id.
    
    # Actually, let's just use the user_id as sender.
    try:
        response = requests.post(RASA_URL, json={"sender": user_data.get("user_id"), "message": user_message})
        response.raise_for_status()
        rasa_data = response.json()
        # print(f"Rasa response: {rasa_data}") # Temporarily disabled to avoid encoding issues
        bot_reply = rasa_data[0]['text'] if rasa_data else "I'm sorry, I couldn't process that."
    except Exception as e:
        print(f"Error in chat route: {str(e).encode('ascii', 'ignore').decode('ascii')}")
        bot_reply = f"AI Server Error: {str(e).encode('ascii', 'ignore').decode('ascii')}"

    # Save conversation in MongoDB with user details and conversation name
    chat_collection.insert_one({
        "user_id": user_data.get("user_id"),
        "conversation_name": conversation_name,
        "user_message": user_message,
        "bot_response": bot_reply,
        "timestamp": datetime.datetime.now()
    })

    return jsonify({"reply": bot_reply})

@app.route("/conversations", methods=["GET"])
@token_required
def get_conversations(user_data):
    user_id = user_data.get("user_id")
    conversations = chat_collection.distinct("conversation_name", {"user_id": user_id})
    return jsonify({"conversations": conversations})

@app.route("/conversation/<name>", methods=["GET"])
@token_required
def get_conversation(user_data, name):
    user_id = user_data.get("user_id")
    messages = list(chat_collection.find(
        {"user_id": user_id, "conversation_name": name},
        {"_id": 0, "user_message": 1, "bot_response": 1, "timestamp": 1}
    ))
    return jsonify({"messages": messages})

@app.route("/rename_conversation", methods=["POST"])
@token_required
def rename_conversation(user_data):
    data = request.json
    old_name = data.get("old_name")
    new_name = data.get("new_name")
    user_id = user_data.get("user_id")
    result = chat_collection.update_many(
        {"user_id": user_id, "conversation_name": old_name},
        {"$set": {"conversation_name": new_name}}
    )
    return jsonify({"modified_count": result.modified_count})

@app.route("/profile", methods=["GET"])
@token_required
def get_profile(user_data):
    user_id = user_data.get("user_id")
    profile = profile_collection.find_one({"user_id": user_id}, {"_id": 0})
    if profile:
        return jsonify({"profile": profile})
    else:
        return jsonify({"profile": None})

@app.route("/profile", methods=["POST"])
@token_required
def update_profile(user_data):
    user_id = user_data.get("user_id")
    data = request.json
    data["user_id"] = user_id
    profile_collection.update_one(
        {"user_id": user_id},
        {"$set": data},
        upsert=True
    )
    return jsonify({"success": True})

@app.route("/outpass/request_internal", methods=["POST"])
def request_outpass_internal():
    from db import users_collection
    from bson import ObjectId
    data = request.json
    # print(f"Internal outpass request received: {data}")
    student_id = data["student_id"]
    
    # Try to fetch real name
    student_name = data.get("student_name")
    if not student_name or student_name == "Student (via Bot)":
        user = users_collection.find_one({"_id": ObjectId(student_id)})
        if user:
            student_name = user.get("name", "Student")
        else:
            student_name = "Student"

    new_outpass = {
        "student_id": student_id,
        "student_name": student_name,
        "type": data.get("type", "outpass"),
        "reason": data["reason"],
        "date_from": data.get("date_from", "N/A"),
        "date_to": data.get("date_to", "N/A"),
        "status": "PENDING",
        "created_at": datetime.datetime.utcnow(),
        "extra_variables": data.get("extra_variables", {})
    }
    db["outpasses"].insert_one(new_outpass)
    return jsonify({"message": "Outpass requested successfully", "id": str(new_outpass["_id"])})
@app.route("/outpass/latest_status", methods=["GET"])
@token_required
def get_latest_outpass_status(user_data):
    user_id = user_data.get("user_id")
    outpass = db["outpasses"].find_one({"student_id": user_id}, sort=[("created_at", -1)])
    if outpass:
        return jsonify({
            "status": outpass["status"],
            "id": str(outpass["_id"]),
            "reason": outpass.get("reason", "N/A"),
            "document": outpass.get("document", "") # The HTML content
        })
    return jsonify({"error": "No outpass found"}), 404

@app.route("/outpass/status_internal", methods=["GET"])
def get_outpass_status_internal():
    student_id = request.args.get("student_id")
    outpasses = list(db["outpasses"].find({"student_id": student_id}).sort("created_at", -1))
    if outpasses:
        results = []
        for o in outpasses:
            results.append({
                "status": o["status"],
                "id": str(o["_id"]),
                "reason": o.get("reason", "N/A"),
                "date": o.get("created_at").strftime("%Y-%m-%d") if o.get("created_at") else "N/A"
            })
        return jsonify({"outpasses": results})
    return jsonify({"error": "No outpass found"}), 404

@app.route("/outpass/download/<id>", methods=["GET"])
def download_outpass_pdf(id):
    from bson import ObjectId
    from xhtml2pdf import pisa
    import io
    from flask import make_response

    outpass = db["outpasses"].find_one({"_id": ObjectId(id)})
    if not outpass:
        return "Not found", 404

    html_content = outpass.get("document", "No content")
    
    # Create a PDF
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html_content.encode("utf-8")), dest=pdf_buffer)
    
    if pisa_status.err:
        return "Error generating PDF", 500
    
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Outpass_{id}.pdf'
    
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=True)
