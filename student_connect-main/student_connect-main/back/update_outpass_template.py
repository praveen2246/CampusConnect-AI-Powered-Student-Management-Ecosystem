from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
templates_collection = db["templates"]

attractive_html = """
<div style="padding: 10px; font-family: 'Helvetica', 'Arial', sans-serif; color: #1e293b;">
    <div style="text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; margin-bottom: 20px;">
        <h1 style="margin: 0; color: #1e3a8a; font-size: 24px; text-transform: uppercase;">Kamaraj College of Engineering and Technology</h1>
        <p style="margin: 5px 0; font-size: 12px; color: #64748b;">(An Autonomous Institution | Accredited by NAAC with 'A' Grade)</p>
        <p style="margin: 2px 0; font-size: 11px; color: #64748b;">Virudhunagar, Tamil Nadu.</p>
    </div>
    
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="display: inline-block; background-color: #1e3a8a; color: #fff; padding: 8px 30px; border-radius: 4px; text-transform: uppercase; font-size: 18px;">STUDENT OUTPASS</h2>
    </div>
    
    <table style="font-size: 14px; margin-bottom: 40px;">
        <tr>
            <td style="width: 30%; font-weight: bold; padding: 8px 0;">Student Name</td>
            <td style="width: 5%;">:</td>
            <td style="border-bottom: 1px solid #cbd5e1; padding: 8px 0; font-weight: bold;">{student_name}</td>
        </tr>
        <tr>
            <td style="font-weight: bold; padding: 8px 0;">Class / Year</td>
            <td>:</td>
            <td style="border-bottom: 1px solid #cbd5e1; padding: 8px 0;">{class}</td>
        </tr>
        <tr>
            <td style="font-weight: bold; padding: 8px 0;">Department</td>
            <td>:</td>
            <td style="border-bottom: 1px solid #cbd5e1; padding: 8px 0;">{department}</td>
        </tr>
        <tr>
            <td style="font-weight: bold; padding: 8px 0;">Departure Case</td>
            <td>:</td>
            <td style="border-bottom: 1px solid #cbd5e1; padding: 8px 0; color: #ef4444; font-weight: bold;">{date_from}</td>
        </tr>
        <tr>
            <td style="font-weight: bold; padding: 8px 0;">Return Date</td>
            <td>:</td>
            <td style="border-bottom: 1px solid #cbd5e1; padding: 8px 0; color: #10b981; font-weight: bold;">{date_to}</td>
        </tr>
        <tr>
            <td style="font-weight: bold; padding: 8px 0;">Reason for Leave</td>
            <td>:</td>
            <td style="border-bottom: 1px solid #cbd5e1; padding: 8px 0;">{reason}</td>
        </tr>
    </table>

    <table style="margin-top: 40px;">
        <tr>
            <td style="width: 45%; text-align: center; border-top: 1px solid #1e3a8a; padding-top: 5px;">
                <p style="font-weight: bold; color: #1e3a8a; margin: 0; font-size: 14px;">Student Signature</p>
            </td>
            <td style="width: 10%;"></td>
            <td style="width: 45%; text-align: center; border-top: 1px solid #1e3a8a; padding-top: 5px;">
                <p style="font-weight: bold; color: #1e3a8a; margin: 0; font-size: 14px;">Authorized Signatory</p>
                <p style="font-size: 10px; color: #64748b; margin: 2px 0 0 0;">(Office of Warden / Principal)</p>
            </td>
        </tr>
    </table>

    <div style="margin-top: 40px; padding: 10px; background-color: #f8fafc; border-left: 4px solid #1e3a8a; font-size: 11px;">
        <p style="margin: 0 0 5px 0; font-weight: bold; color: #1e3a8a;">Instructions:</p>
        <p style="margin: 0;">1. This outpass is valid ONLY for the dates mentioned.</p>
        <p style="margin: 0;">2. Present this document at the Security Gate while leaving and entering.</p>
        <p style="margin: 0;">3. Misuse will lead to disciplinary action.</p>
    </div>
</div>
"""

templates_collection.update_one(
    {"type": "outpass"},
    {"$set": {
        "content": attractive_html,
        "variables": ["student_name", "class", "department", "date_from", "date_to", "reason"]
    }},
    upsert=True
)

print("Attractive Outpass Template Updated Successfully!")
