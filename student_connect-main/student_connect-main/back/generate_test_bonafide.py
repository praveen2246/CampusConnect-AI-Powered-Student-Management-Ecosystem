from pymongo import MongoClient
import os
from dotenv import load_dotenv
from xhtml2pdf import pisa
from bson import ObjectId

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Generate a dummy bonafide if none exists
bonafide = db["outpasses"].find_one({"type": "bonafide", "status": "APPROVED"})
if not bonafide:
    print("No approved bonafide found. Fetching any one or using template.")
    tmpl = db["templates"].find_one({"type": "bonafide"})
    doc_content = tmpl["content"]
    # Dummy replacement
    doc_content = doc_content.replace("{student_name}", "John Doe")
    doc_content = doc_content.replace("{roll_no}", "21CS101")
    doc_content = doc_content.replace("{department}", "Computer Science and Engineering")
    doc_content = doc_content.replace("{academic_year}", "2023-2024")
    doc_content = doc_content.replace("{reason}", "Internship")
    doc_content = doc_content.replace("{date_now}", "23/02/2026")
else:
    doc_content = bonafide["document"]

output_filename = "test_bonafide.pdf"
with open(output_filename, "wb") as f:
    pisa_status = pisa.CreatePDF(doc_content, dest=f)

print(f"PDF generated: {os.path.abspath(output_filename)}")
if pisa_status.err:
    print("Error during PDF generation!")
