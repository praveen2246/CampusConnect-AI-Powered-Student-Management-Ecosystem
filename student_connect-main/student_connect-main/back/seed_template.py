from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client[os.getenv("MONGO_DB_NAME", "college_chatbot")]
templates_collection = db["templates"]

professional_html = """
<html>
<head>
    <style>
        @page {
            size: a4 portrait;
            margin: 1.5cm;
        }
        body {
            font-family: Arial, sans-serif;
            color: #1e293b;
        }
        .header-table {
            width: 100%;
            border-bottom: 3px solid #000000;
            margin-bottom: 30px;
        }
        .college-name {
            color: #000000;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
        }
        .title {
            text-align: center;
            font-size: 20px;
            text-decoration: underline;
            margin-bottom: 40px;
            color: #000000;
        }
        .info-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 60px;
        }
        .info-table td {
            padding: 10px;
            font-size: 16px;
        }
        .label {
            font-weight: bold;
            width: 35%;
        }
        .value {
            border-bottom: 1px solid #94a3b8;
        }
        .signature-table {
            width: 100%;
            margin-top: 100px;
        }
        .signature-box {
            border-top: 1px solid #1e293b;
            padding-top: 10px;
            text-align: center;
            width: 250px;
        }
        .footer {
            text-align: center;
            font-size: 10px;
            color: #64748b;
            margin-top: 50px;
            border-top: 1px dashed #cbd5e1;
            padding-top: 10px;
        }
    </style>
</head>
<body>
    <table class="header-table">
        <tr>
            <td class="college-name">Kamaraj College of Engineering and Technology</td>
        </tr>
    </table>

    <div class="title">STUDENT OUTPASS</div>

    <table class="info-table">
        <tr>
            <td class="label">Student Name</td>
            <td>:</td>
            <td class="value">{student_name}</td>
        </tr>
        <tr>
            <td class="label">Class / Year</td>
            <td>:</td>
            <td class="value">{class}</td>
        </tr>
        <tr>
            <td class="label">Out Date & Time</td>
            <td>:</td>
            <td class="value">{date_from}</td>
        </tr>
        <tr>
            <td class="label">In Date & Time</td>
            <td>:</td>
            <td class="value">{date_to}</td>
        </tr>
        <tr>
            <td class="label">Reason</td>
            <td>:</td>
            <td class="value">{reason}</td>
        </tr>
    </table>

    <table class="signature-table">
        <tr>
            <td style="width: 60%;"></td>
            <td>
                <div class="signature-box">
                    <strong>Warden Signature</strong>
                </div>
            </td>
        </tr>
    </table>

    <div class="footer">
        Computer Generated Outpass | Campus Connect Portal
    </div>
</body>
</html>
"""

bonafide_html = """
<html>
<head>
    <style>
        @page {
            size: a4 portrait;
            margin: 1cm;
        }
        body {
            font-family: 'Times New Roman', Times, serif;
            color: #000;
        }
        .container {
            padding: 20px;
        }
        .college-header {
            text-align: center;
            border-bottom: 2px solid #000;
            margin-bottom: 25px;
            padding-bottom: 12px;
        }
        .college-name {
            font-size: 24pt;
            font-weight: bold;
            color: #000;
        }
        .college-info {
            font-size: 11pt;
            color: #333;
        }
        .cert-title {
            text-align: center;
            font-size: 20pt;
            font-weight: bold;
            text-decoration: underline;
            margin: 40px 0;
        }
        .date-line {
            font-size: 12pt;
            margin-bottom: 25px;
        }
        .main-text {
            font-size: 14pt;
            text-align: justify;
            margin-bottom: 60px;
            line-height: 1.8;
        }
        .sig-table {
            width: 100%;
            margin-top: 60px;
        }
        .sig-box {
            text-align: center;
            font-size: 11pt;
            font-weight: bold;
        }
        .sig-line {
            border-top: 1px solid #000;
            margin: 0 15px;
            padding-top: 8px;
        }
        .footer-note {
            text-align: center;
            font-size: 9pt;
            color: #555;
            margin-top: 80px;
            border-top: 1px dashed #999;
            padding-top: 10px;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="college-header">
        <div class="college-name">Kamaraj College of Engineering and Technology</div>
        <div class="college-info">
            (An Autonomous Institution | Approved by AICTE, New Delhi)<br/>
            S.P.G.Chidambara Nadar - C.Nagammal Campus, Madurai - 625 701.<br/>
            Phone: 04549 278171 | Email: mail@kamarajengg.edu.in
        </div>
    </div>

    <div class="cert-title">BONAFIDE CERTIFICATE</div>

    <table style="width: 100%; margin-bottom: 25px;">
        <tr>
            <td style="font-size: 13pt;"><strong>Date:</strong> {date_now}</td>
        </tr>
    </table>

    <div class="main-text">
        This is to certify that <strong>{student_name}</strong>, bearing Register Number <strong>{roll_no}</strong>, 
        is a bonafide student of <strong>{department}</strong> at <strong>Kamaraj College of Engineering and Technology</strong> 
        for the academic year <strong>{academic_year}</strong>. This certificate is issued upon the request of the student 
        for <strong>{reason}</strong>.
    </div>

    <div style="text-align: center; margin-bottom: 60px;">
        <div style="width: 130px; height: 130px; border: 1px dashed #666; display: inline-block; padding-top: 55px; font-size: 9pt; color: #666;">
            OFFICIAL STAMP
        </div>
    </div>

    <table class="sig-table">
        <tr>
            <td style="width: 33.3%;">
                <div class="sig-box">
                    <div class="sig-line">Class Advisor</div>
                </div>
            </td>
            <td style="width: 33.3%;">
                <div class="sig-box">
                    <div class="sig-line">Head of Department</div>
                </div>
            </td>
            <td style="width: 33.3%;">
                <div class="sig-box">
                    <div class="sig-line">Principal</div>
                </div>
            </td>
        </tr>
    </table>

    <div class="footer-note">
        This is a computer-generated document. Verification can be done via the Campus Connect Portal.
    </div>
</div>
</body>
</html>
"""

grade_certificate_html = """
<html>
<head>
    <style>
        @page {
            size: a4 portrait;
            margin: 0.8cm;
        }
        body {
            font-family: 'Times New Roman', Times, serif;
            color: #1e293b;
            line-height: 1.2;
            font-size: 11pt;
        }
        .container {
            border: 1.5px solid #1e3a8a;
            padding: 15px;
        }
        .header {
            text-align: center;
            border-bottom: 1.5px solid #1e3a8a;
            padding-bottom: 5px;
            margin-bottom: 20px;
        }
        .college-name {
            font-size: 20pt;
            font-weight: bold;
            color: #1e3a8a;
            text-transform: uppercase;
        }
        .title {
            text-align: center;
            font-size: 16pt;
            font-weight: bold;
            margin: 10px 0;
            text-decoration: underline;
        }
        .info-table {
            width: 100%;
            margin-bottom: 15px;
        }
        .info-table td {
            padding: 3px;
            font-size: 11pt;
        }
        .label {
            font-weight: bold;
            width: 30%;
        }
        .grade-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        .grade-table th, .grade-table td {
            border: 1px solid #1e3a8a;
            padding: 6px;
            text-align: center;
            font-size: 10pt;
        }
        .grade-table th {
            background-color: #f1f5f9;
        }
        .gpa-container {
            text-align: right;
            font-size: 14pt;
            font-weight: bold;
            margin-top: 10px;
            color: #1e3a8a;
        }
        .footer {
            margin-top: 40px;
            width: 100%;
        }
        .sig-box {
            text-align: center;
            width: 180px;
            font-size: 10pt;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="college-name">Kamaraj College of Engineering and Technology</div>
        <div style="font-size: 10pt;">(An Autonomous Institution)</div>
        <div style="font-size: 10pt;">S.P.G.C. Nagar, K. Vellakulam - 625 701</div>
    </div>

    <div class="title">STUDENT GRADE CERTIFICATE</div>

    <table class="info-table">
        <tr>
            <td class="label">First Name</td>
            <td>: {student_name}</td>
        </tr>
        <tr>
            <td class="label">Register Number</td>
            <td>: {roll_no}</td>
        </tr>
        <tr>
            <td class="label">Class</td>
            <td>: {class}</td>
        </tr>
        <tr>
            <td class="label">Academic Year</td>
            <td>: {academic_year}</td>
        </tr>
    </table>

    <table class="grade-table">
        <thead>
            <tr>
                <th>Subject Name</th>
                <th>Grade Obtained</th>
            </tr>
        </thead>
        <tbody>
            {subjects_table_rows}
        </tbody>
    </table>

    <div class="gpa-container">
        GPA: {cgpa}
    </div>

    <table class="footer">
        <tr>
            <td>
                <div class="sig-box">
                    <p>____________________</p>
                    <p><b>Prepared By</b></p>
                </div>
            </td>
            <td style="text-align: right;">
                <div class="sig-box" style="float: right;">
                    <p>____________________</p>
                    <p><b>Controller of Examinations</b></p>
                </div>
            </td>
        </tr>
    </table>
    
    <div style="margin-top: 30px; text-align: center; font-size: 9pt; color: #64748b;">
        Date of Issue: {date_now}
    </div>
</div>
</body>
</html>
"""

# Seed Outpass Template
templates_collection.update_one(
    {"type": "outpass"},
    {"$set": {
        "content": professional_html,
        "variables": ["student_name", "class", "date_from", "date_to", "reason"]
    }},
    upsert=True
)

# Seed Bonafide Template
templates_collection.update_one(
    {"type": "bonafide"},
    {"$set": {
        "content": bonafide_html,
        "variables": ["student_name", "roll_no", "department", "academic_year", "reason", "date_now"]
    }},
    upsert=True
)

# Seed Grade Certificate Template
templates_collection.update_one(
    {"type": "grade_certificate"},
    {"$set": {
        "content": grade_certificate_html,
        "variables": ["student_name", "roll_no", "class", "academic_year", "subjects_table_rows", "cgpa", "date_now"]
    }},
    upsert=True
)

print("Professional Templates Seeded Successfully!")
