from pymongo import MongoClient
import os
from dotenv import load_dotenv
from xhtml2pdf import pisa
import io
import traceback

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "college_chatbot")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
outpass_collection = db["outpasses"]

# Fetch the latest outpass
outpass = outpass_collection.find_one(sort=[("created_at", -1)])

if not outpass:
    print("No outpass found to test.")
    exit()

print(f"Testing PDF generation for outpass: {outpass['_id']}")
html_content = outpass.get("document", "")

print("HTML Content Length:", len(html_content))
print("First 100 chars:", html_content[:100])

# Test 1: Minimal Hello World
print("\n--- Test 1: Minimal Hello World ---")
try:
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(b"<html><body><h1>Hello World</h1></body></html>"), dest=pdf_buffer)
    if not pisa_status.err:
        print("Success! Minimal PDF size:", len(pdf_buffer.getvalue()))
    else:
        print("Failed minimal test.")
except Exception:
    traceback.print_exc()

# Test 2: Revised Template (No width: 100%)
print("\n--- Test 2: Revised Template ---")
revised_html = html_content.replace('width: 100%;', '') # Try removing width: 100%
# Also remove padding that might cause overflow
revised_html = revised_html.replace('padding: 20px;', 'padding: 5px;')

try:
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(revised_html.encode("utf-8")), dest=pdf_buffer)
    
    if pisa_status.err:
        print("pisa_status.err reported an error!")
    else:
        print("Success! Revised PDF size:", len(pdf_buffer.getvalue()))
        # If success, we should use this revised HTML
        
except Exception:
    print("Caught Exception during Revised Template Generation:")
    traceback.print_exc()
