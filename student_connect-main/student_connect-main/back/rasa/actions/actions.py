from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionStartCertificateRequest(Action):
    def name(self) -> Text:
        return "action_start_certificate_request"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cert_type = tracker.get_slot("cert_type") or "outpass"
        backend_url = f"http://127.0.0.1:8000/admin/templates?type={cert_type}"
        
        try:
            res = requests.get(backend_url)
            if res.status_code == 200:
                data = res.json()
                variables = data.get("variables", [])
                
                # We need to ask for variables that aren't already set
                for var in variables:
                    if not tracker.get_slot(var) and var != "student_name":
                        dispatcher.utter_message(text=f"Please provide the value for: {var.replace('_', ' ')}")
                        return [] # Stop here so user can answer
            
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []

class ActionSubmitOutpass(Action):
    def name(self) -> Text:
        return "action_submit_outpass"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_id = tracker.sender_id
        cert_type = tracker.get_slot("cert_type") or "outpass"
        
        # Collect all typical slots + generic ones if any
        payload = {
            "student_id": user_id,
            "student_name": tracker.get_slot("student_name") or "Student",
            "type": "outpass",
            "reason": tracker.get_slot("outpass_reason") or tracker.get_slot("reason"),
            "date_from": tracker.get_slot("outpass_from") or tracker.get_slot("date_from"),
            "date_to": tracker.get_slot("outpass_to") or tracker.get_slot("date_to"),
            "extra_variables": {
                "class": tracker.get_slot("class"),
                "department": tracker.get_slot("department")
            }
        }
        
        # Add any other slots that might have been filled
        for slot_name, slot_value in tracker.slots.items():
            if slot_value and slot_name not in ["session_started_metadata", "student_id"]:
                payload["extra_variables"][slot_name] = slot_value
        
        backend_url = "http://127.0.0.1:8000/outpass/request_internal" 
        
        try:
            response = requests.post(backend_url, json=payload)
            if response.status_code == 200:
                print(f"Request for {cert_type} submitted successfully")
                dispatcher.utter_message(text=f"[SUCCESS] Your {cert_type} request has been submitted successfully for approval!")
            else:
                print(f"Failed to submit: {response.status_code}")
                dispatcher.utter_message(text="[ERROR] I'm sorry, I couldn't submit your request at this moment. Please try again later.")
        except Exception as e:
            print(f"Error calling backend: {e}")

        return []

class ActionSubmitBonafide(Action):
    def name(self) -> Text:
        return "action_submit_bonafide"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_id = tracker.sender_id
        cert_type = "bonafide"
        
        payload = {
            "student_id": user_id,
            "type": cert_type,
            "reason": tracker.get_slot("bonafide_reason") or tracker.get_slot("reason"),
            "extra_variables": {}
        }
        
        # Add any other slots that might have been filled
        for slot_name, slot_value in tracker.slots.items():
            if slot_value and slot_name not in ["session_started_metadata", "student_id", "bonafide_reason"]:
                payload["extra_variables"][slot_name] = slot_value
        
        payload["student_id"] = user_id # Ensure it's there
        print(f"Submitting Bonafide payload: {payload}")
        
        backend_url = "http://127.0.0.1:8000/outpass/request_internal" 
        
        try:
            response = requests.post(backend_url, json=payload)
            if response.status_code == 200:
                print(f"Request for {cert_type} submitted successfully")
                dispatcher.utter_message(text=f"[SUCCESS] Your {cert_type} certificate request has been submitted successfully for approval!")
            else:
                print(f"Failed to submit: {response.status_code}")
                dispatcher.utter_message(text="[ERROR] I'm sorry, I couldn't submit your request at this moment. Please try again later.")
        except Exception as e:
            print(f"Error calling backend: {e}")

        return []

class ActionCheckOutpassStatus(Action):
    def name(self) -> Text:
        return "action_check_outpass_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_id = tracker.sender_id
        backend_url = f"http://127.0.0.1:8000/outpass/status_internal?student_id={user_id}"
        
        try:
            res = requests.get(backend_url)
            if res.status_code == 200:
                data = res.json()
                outpasses = data.get("outpasses", [])
                
                if not outpasses:
                    dispatcher.utter_message(text="I couldn't find any outpass requests for you. Would you like to apply for one?")
                    return []

                msg = "Your Outpass Applications:\n\n"
                latest_approved_id = None
                
                for idx, o in enumerate(outpasses[:5]): # Show last 5
                    status_icon = "(WAITING)"
                    if o['status'] == "APPROVED": status_icon = "(APPROVED)"
                    if o['status'] == "REJECTED": status_icon = "(REJECTED)"
                    
                    msg += f"{idx+1}. {o['reason']}\n"
                    msg += f"   Status: {o['status']} {status_icon}\n"
                    msg += f"   Requested on: {o['date']}\n\n"
                    
                    if o['status'] == "APPROVED" and latest_approved_id is None:
                        latest_approved_id = o['id']

                dispatcher.utter_message(text=msg)
                
                if latest_approved_id:
                    dispatcher.utter_message(text=f"Found your most recent approved outpass! You can download the PDF here: http://127.0.0.1:8000/outpass/download/{latest_approved_id}")
                else:
                    dispatcher.utter_message(text="Note: Only approved outpasses are available for PDF download.")
            else:
                dispatcher.utter_message(text="I couldn't find any recent outpass requests for you. Would you like to apply for one?")
            
            return []
        except Exception as e:
            print(f"Error checking status: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the records right now.")
            return []
