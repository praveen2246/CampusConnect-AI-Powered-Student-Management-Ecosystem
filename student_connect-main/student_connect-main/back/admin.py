from flask import Blueprint, request, jsonify
from db import db, users_collection
from werkzeug.security import check_password_hash
import jwt
import datetime
import os
from bson import ObjectId

admin_bp = Blueprint('admin', __name__)
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
outpass_collection = db["outpasses"]
templates_collection = db["templates"]

@admin_bp.route("/login", methods=["POST"])
def admin_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    user = users_collection.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
         return jsonify({"error": "Invalid credentials"}), 401
    
    if user.get("role") != "admin":
         return jsonify({"error": "Access denied. Not an admin."}), 403

    token = jwt.encode({
        "user_id": str(user["_id"]),
        "role": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, SECRET_KEY, algorithm="HS256")
    
    return jsonify({"token": token, "name": user["name"], "role": "admin"})

@admin_bp.route("/templates/list", methods=["GET"])
def list_template_types():
    types = templates_collection.distinct("type")
    # Ensure defaults are there if empty
    if not types:
        types = ["outpass", "bonafide", "leave"]
    return jsonify(types)

@admin_bp.route("/templates", methods=["GET", "POST"])
def manage_templates():
    if request.method == "POST":
        data = request.json
        t_type = data.get("type", "outpass")
        templates_collection.update_one(
            {"type": t_type}, 
            {"$set": {
                "content": data["content"],
                "variables": data.get("variables", ["student_name", "reason", "date_from", "date_to"])
            }}, 
            upsert=True
        )
        return jsonify({"message": "Template saved"})
    else:
        t_type = request.args.get("type", "outpass")
        tmpl = templates_collection.find_one({"type": t_type})
        if tmpl:
            return jsonify({
                "content": tmpl["content"],
                "variables": tmpl.get("variables", ["student_name", "reason", "date_from", "date_to"])
            })
        else:
            return jsonify({
                "content": f"Official template for {t_type}.",
                "variables": ["student_name", "reason", "date_from", "date_to"]
            })

@admin_bp.route("/outpasses", methods=["GET"])
def get_outpasses():
    # In a real app, verify JWT admin token here
    outpasses = list(outpass_collection.find().sort("created_at", -1))
    for o in outpasses:
        o["_id"] = str(o["_id"])
    return jsonify(outpasses)

@admin_bp.route("/outpasses/<id>", methods=["PUT"])
def update_outpass(id):
    data = request.json
    status = data.get("status") # APPROVED, REJECTED
    
    if status == "APPROVED":
        # Generate document content based on template
        outpass = outpass_collection.find_one({"_id": ObjectId(id)})
        cert_type = outpass.get("type", "outpass")
        
        tmpl = templates_collection.find_one({"type": cert_type})
        if tmpl:
            tmpl_content = tmpl["content"]
        else:
            # Enhanced default template with College Name
            tmpl_content = f"""
            <div style="text-align: center; font-family: Arial, sans-serif;">
                <h1 style="color: #1e3a8a;">Kamaraj College of Engineering and Technology</h1>
                <hr/>
                <h2 style="text-transform: uppercase;">Official {cert_type.replace('_', ' ')}</h2>
                <div style="text-align: left; margin-top: 40px; line-height: 1.6;">
                    <p>This is to certify that <b>{{student_name}}</b> is permitted for <b>{{reason}}</b>.</p>
                    <p><b>Duration:</b> {{date_from}} to {{date_to}}</p>
                </div>
                <div style="margin-top: 60px; text-align: right;">
                    <p>____________________</p>
                    <p><b>Authorized Signatory</b></p>
                </div>
            </div>
            """
        student_id = outpass.get("student_id")
        
        # Fetch profile data for better variables
        profile_data = db["profile"].find_one({"user_id": student_id}) or {}
        
        # Merge all available data for replacement
        extra_vars = outpass.get("extra_variables", {})
        replace_map = {
            "student_name": outpass.get("student_name") or profile_data.get("Name") or "Student",
            "date_from": outpass.get("date_from") or "N/A",
            "date_to": outpass.get("date_to") or "N/A",
            "reason": outpass.get("reason") or "N/A",
            "roll_no": extra_vars.get("roll_no") or profile_data.get("Roll No.") or "N/A",
            "department": extra_vars.get("department") or profile_data.get("Department") or "N/A",
            "class": extra_vars.get("class") or extra_vars.get("class_year") or profile_data.get("Class") or "N/A",
            "semester": extra_vars.get("semester") or "N/A",
            "academic_year": extra_vars.get("academic_year") or "2023-2024",
            "exam_name": extra_vars.get("exam_name") or "Semester Examination",
            "subjects_table_rows": extra_vars.get("subjects_table_rows") or "<tr><td colspan='2'>No results provided</td></tr>",
            "cgpa": extra_vars.get("cgpa") or "0.00",
            "gender": profile_data.get("Gender") or "N/A",
            "contact": profile_data.get("Father Mobile No.") or "N/A",
            "created_at": outpass.get("created_at").strftime("%Y-%m-%d %H:%M:%S") if outpass.get("created_at") else "N/A",
            "date_now": datetime.datetime.now().strftime("%d/%m/%Y")
        }

        doc_content = tmpl_content
        for key, val in replace_map.items():
            placeholder = "{" + key + "}"
            doc_content = doc_content.replace(placeholder, str(val))
            
        outpass_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": "APPROVED", "document": doc_content}})
    else:
        outpass_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})
        
    return jsonify({"message": f"Outpass {status}"})
