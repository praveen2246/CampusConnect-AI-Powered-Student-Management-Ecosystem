import requests
import json
import time

def test_bonafide_flow():
    url = "http://localhost:5005/webhooks/rest/webhook"
    sender_id = f"verification_user_{int(time.time())}"
    
    steps = [
        ("apply for bonafide", "Start Flow"),
        ("Final Verify Student", "Name"),
        ("REG-TEST-001", "Reg No"),
        ("23/02/2026", "Date"),
        ("2023-2024", "Academic Year"),
        ("Final Verification", "Reason"),
        ("Yes", "Confirm")
    ]
    
    print(f"Testing with Sender ID: {sender_id}")
    for msg, label in steps:
        print(f"--- User ({label}): {msg} ---")
        try:
            res = requests.post(url, json={"sender": sender_id, "message": msg}, timeout=10)
            if res.status_code == 200:
                responses = res.json()
                for r in responses:
                    text = r.get('text')
                    if text:
                        print(f"Bot: {text}")
            else:
                print(f"Error: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"Exception: {e}")
        time.sleep(1.5)

if __name__ == "__main__":
    test_bonafide_flow()
