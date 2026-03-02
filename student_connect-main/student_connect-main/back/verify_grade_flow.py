import requests
import json
import time

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"
SENDER_ID = "test_student_simplified"

def send_message(message):
    print(f"User: {message}")
    payload = {"sender": SENDER_ID, "message": message}
    try:
        response = requests.post(RASA_URL, json=payload)
        response.raise_for_status()
        messages = response.json()
        for msg in messages:
            if "text" in msg:
                print(f"Bot: {msg['text']}")
        return messages
    except Exception as e:
        print(f"Error: {e}")
        return []

def run_verification():
    print("Starting Simplified Grade Certificate Flow Verification...")
    
    # 1. Start application
    send_message("apply for grade certificate")
    time.sleep(1)
    
    # 2. First Name
    send_message("Simplified")
    time.sleep(1)
    
    # 3. Register Number
    send_message("SIMP789")
    time.sleep(1)
    
    # 4. Class
    send_message("B.Sc Computer Science / III CSE")
    time.sleep(1)
    
    # 5. Academic Year
    send_message("2023-2024")
    time.sleep(1)
    
    # 6. Number of Subjects
    send_message("3")
    time.sleep(1)
    
    # 7. Grade 1
    send_message("O")
    time.sleep(1)
    
    # 8. Grade 2
    send_message("A+")
    time.sleep(1)
    
    # 9. Grade 3
    send_message("A")
    time.sleep(1)
    
    # 10. Date of Issue
    send_message("23/02/2026")
    time.sleep(1)
    
    # 11. Final confirmation
    send_message("yes")
    time.sleep(2)
    
    print("\nVerification session complete.")

if __name__ == "__main__":
    run_verification()
