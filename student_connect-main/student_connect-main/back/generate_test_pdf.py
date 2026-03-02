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

outpass = db["outpasses"].find_one(sort=[("created_at", -1)])
if outpass and "document" in outpass:
    html_content = outpass["document"]
    output_filename = "test_outpass.pdf"
    with open(output_filename, "wb") as f:
        pisa_status = pisa.CreatePDF(html_content, dest=f)
    print(f"PDF generated: {os.path.abspath(output_filename)}")
    if pisa_status.err:
        print("Error during PDF generation!")
else:
    print("No outpass with document found.")
