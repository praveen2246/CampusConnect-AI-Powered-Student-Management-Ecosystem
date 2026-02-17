from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client[os.getenv("MONGO_DB_NAME", "college_chatbot")]
templates_collection = db["templates"]

professional_html = """
<div style="font-family: 'Helvetica', 'Arial', sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; border: 15px solid #1e3a8a; background-color: #ffffff; color: #1e293b; position: relative;">
    <!-- Background Watermark (Optional, simplified for xhtml2pdf) -->
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="margin: 0; color: #1e3a8a; font-size: 32px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">Kamaraj College</h1>
        <p style="margin: 5px 0; font-size: 14px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 2px;">of Engineering and Technology</p>
        <p style="margin: 2px 0; font-size: 11px; color: #94a3b8;">(An Autonomous Institution | Approved by AICTE, New Delhi)</p>
        <div style="margin-top: 15px; border-bottom: 3px double #1e3a8a; width: 80%; margin-left: auto; margin-right: auto;"></div>
    </div>

    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="margin: 0; font-size: 24px; color: #1e3a8a; background-color: #f1f5f9; display: inline-block; padding: 10px 30px; border-radius: 4px; border: 1px solid #cbd5e1; text-transform: uppercase;">Student Outpass</h2>
    </div>

    <div style="line-height: 1.8; font-size: 16px; margin-bottom: 40px;">
        <p>This is to certify that <strong>{student_name}</strong>, a bona-fide student of this institution, is permitted to leave the premises as per the details mentioned below:</p>
    </div>

    <table style="width: 100%; border-collapse: collapse; margin-bottom: 40px; border: 1px solid #e2e8f0;">
        <tr style="background-color: #f8fafc;">
            <th style="text-align: left; padding: 12px 15px; border: 1px solid #e2e8f0; color: #475569; width: 35%;">Purpose of Visit</th>
            <td style="padding: 12px 15px; border: 1px solid #e2e8f0; font-weight: 600;">{reason}</td>
        </tr>
        <tr>
            <th style="text-align: left; padding: 12px 15px; border: 1px solid #e2e8f0; color: #475569;">Departure Date & Time</th>
            <td style="padding: 12px 15px; border: 1px solid #e2e8f0; font-weight: 600;">{date_from}</td>
        </tr>
        <tr style="background-color: #f8fafc;">
            <th style="text-align: left; padding: 12px 15px; border: 1px solid #e2e8f0; color: #475569;">Expected Return</th>
            <td style="padding: 12px 15px; border: 1px solid #e2e8f0; font-weight: 600;">{date_to}</td>
        </tr>
    </table>

    <div style="margin-top: 60px; height: 120px;">
        <table style="width: 100%;">
            <tr>
                <td style="width: 50%; text-align: center;">
                    <div style="margin-bottom: 10px; font-weight: bold; height: 40px;"></div>
                    <div style="border-top: 1px solid #94a3b8; width: 180px; margin: 0 auto; padding-top: 5px;">
                        <p style="margin: 0; font-size: 14px; font-weight: 700;">Student Signature</p>
                    </div>
                </td>
                <td style="width: 50%; text-align: center;">
                    <div style="margin-bottom: 5px; color: #1e3a8a; font-weight: 800; font-size: 14px; height: 40px; vertical-align: bottom;">DIGITALLY VERIFIED</div>
                    <div style="border-top: 2px solid #1e3a8a; width: 220px; margin: 0 auto; padding-top: 5px;">
                        <p style="margin: 0; font-size: 14px; font-weight: 700;">Warden / HOD / Principal</p>
                        <p style="margin: 0; font-size: 10px; color: #64748b;">(Generated via Student Connect Portal)</p>
                    </div>
                </td>
            </tr>
        </table>
    </div>

    <div style="margin-top: 50px; padding: 15px; background-color: #fff7ed; border: 1px solid #fed7aa; border-radius: 4px; font-size: 11px; color: #9a3412;">
        <strong>Important Instructions:</strong>
        <ul style="margin: 5px 0 0 20px; padding: 0;">
            <li>This document must be presented at the Security Desk upon departure and arrival.</li>
            <li>Any deviation from the mentioned schedule or purpose will attract disciplinary action.</li>
            <li>In case of emergency, contact the institutional helpline immediately.</li>
        </ul>
    </div>
    
    <div style="margin-top: 20px; text-align: center; font-size: 10px; color: #94a3b8;">
        Document ID: <span style="font-family: monospace;">CERT-{student_name[:3].upper()}-{date_from.replace('-', '')}</span> | College Copy
    </div>
</div>
"""

templates_collection.update_one(
    {"type": "outpass"},
    {"$set": {
        "content": professional_html,
        "variables": ["student_name", "reason", "date_from", "date_to"]
    }},
    upsert=True
)

print("Professional Outpass Template Seeded Successfully!")
