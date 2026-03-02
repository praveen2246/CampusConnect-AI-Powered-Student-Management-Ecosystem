from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, FollowupAction
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

class ActionStartCertificateRequest(Action):
    def name(self) -> Text:
        return "action_start_certificate_request"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text=(
            "Sure! Which certificate would you like to apply for?\n\n"
            "1️⃣ Type **apply for outpass** — for Outpass\n"
            "2️⃣ Type **apply for bonafide** — for Bonafide Certificate\n"
            "3️⃣ Type **apply for grade certificate** — for Grade Certificate / Mark Sheet"
        ))
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
        
        # Pull data from the new bonafide slots
        student_name = tracker.get_slot("bonafide_full_name") or tracker.get_slot("student_name")
        roll_no = tracker.get_slot("bonafide_register_number") or tracker.get_slot("roll_no")
        academic_year = tracker.get_slot("bonafide_academic_year")
        date_now = tracker.get_slot("bonafide_date")
        reason = tracker.get_slot("bonafide_reason")

        payload = {
            "student_id": user_id,
            "student_name": student_name,
            "type": cert_type,
            "reason": reason,
            "extra_variables": {
                "roll_no": roll_no,
                "academic_year": academic_year,
                "date_now": date_now,
                "department": tracker.get_slot("department") or "Engineering"
            }
        }
        
        print(f"Submitting Bonafide payload: {payload}")
        backend_url = "http://127.0.0.1:8000/outpass/request_internal" 
        
        try:
            response = requests.post(backend_url, json=payload)
            if response.status_code == 200:
                dispatcher.utter_message(template="utter_bonafide_submitted")
            else:
                dispatcher.utter_message(text="[ERROR] I'm sorry, I couldn't submit your request. Please try again later.")
        except Exception as e:
            print(f"Error calling backend: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the system.")

        # Reset bonafide slots after submission
        return [
            SlotSet("bonafide_full_name", None),
            SlotSet("bonafide_register_number", None),
            SlotSet("bonafide_date", None),
            SlotSet("bonafide_academic_year", None),
            SlotSet("bonafide_reason", None)
        ]

class ActionResetBonafideSlots(Action):
    def name(self) -> Text:
        return "action_reset_bonafide_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            SlotSet("bonafide_full_name", None),
            SlotSet("bonafide_register_number", None),
            SlotSet("bonafide_date", None),
            SlotSet("bonafide_academic_year", None),
            SlotSet("bonafide_reason", None)
        ]

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
                    dispatcher.utter_message(text=f"Found your most recent approved outpass! You can download the PDF here: http://localhost:8000/outpass/download/{latest_approved_id}")
                else:
                    dispatcher.utter_message(text="Note: Only approved outpasses are available for PDF download.")
            else:
                dispatcher.utter_message(text="I couldn't find any recent outpass requests for you. Would you like to apply for one?")
            
            return []
        except Exception as e:
            print(f"Error checking status: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the records right now.")
            return []

class ActionCalculateGPA(Action):
    def name(self) -> Text:
        # Keep name action_calculate_cgpa for compatibility with rules unless I change rules.yml too.
        # I'll change it to action_calculate_cgpa to avoid breaking rules.yml for now.
        return "action_calculate_cgpa"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        grades_list = tracker.get_slot("grade_subjects_grades_list")
        if not grades_list:
            return [SlotSet("grade_gpa", "0.00")]

        # Grade Point Mapping
        grade_points = {
            "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6
        }

        total_points = 0
        subject_count = 0
        
        for grade in grades_list:
            grade_val = grade.upper()
            point = grade_points.get(grade_val, 0)
            total_points += point
            subject_count += 1

        gpa_val = "{:.2f}".format(total_points / subject_count) if subject_count > 0 else "0.00"
        
        # Format the grades into a simple comma-separated string for summary
        grades_raw = ", ".join(grades_list)
        
        return [SlotSet("grade_gpa", gpa_val), SlotSet("grade_subjects_grades", grades_raw)]

class ValidateGradeCertificateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_grade_certificate_form"

    def validate_grade_num_subjects(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            num = int(slot_value)
            if num <= 0:
                dispatcher.utter_message(text="Please enter a positive number of subjects.")
                return {"grade_num_subjects": None}
            return {
                "grade_num_subjects": num, 
                "grade_current_index": 1, 
                "grade_subjects_grades_list": []
            }
        except:
            dispatcher.utter_message(text="Please enter a valid number.")
            return {"grade_num_subjects": None}

    def validate_grade_current_subject_grade(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        grade_points = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6}
        grade = slot_value.upper()
        if grade not in grade_points:
            dispatcher.utter_message(text="Invalid grade. Please enter one of: O, A+, A, B+, B.")
            return {"grade_current_subject_grade": None}

        current_list = tracker.get_slot("grade_subjects_grades_list") or []
        current_index = int(tracker.get_slot("grade_current_index") or 1)
        num_subjects = int(tracker.get_slot("grade_num_subjects") or 0)
        
        current_list.append(grade)
        
        if current_index < num_subjects:
            # Reset only the grade slot for the next iteration
            return {
                "grade_current_subject_grade": None,
                "grade_subjects_grades_list": current_list,
                "grade_current_index": current_index + 1
            }
        else:
            # Done collecting all grades
            return {
                "grade_current_subject_grade": grade,
                "grade_subjects_grades_list": current_list
            }

class ActionSubmitGradeCertificate(Action):
    def name(self) -> Text:
        return "action_submit_grade_certificate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_id = tracker.sender_id
        cert_type = "grade_certificate"
        
        subjects_list = tracker.get_slot("grade_subjects_grades_list")
        first_name = tracker.get_slot("grade_first_name")
        reg_no = tracker.get_slot("grade_register_number")
        grade_class = tracker.get_slot("grade_class")
        academic_year = tracker.get_slot("grade_academic_year")
        date_now = tracker.get_slot("grade_date")
        gpa = tracker.get_slot("grade_gpa") or "0.00"

        # Format table rows from list of grades
        table_rows_html = ""
        for idx, grade in enumerate(subjects_list):
            table_rows_html += f"<tr><td>Subject {idx+1}</td><td>{grade}</td></tr>"

        payload = {
            "student_id": user_id,
            "student_name": first_name,
            "type": cert_type,
            "reason": f"Grade Certificate for {academic_year}",
            "extra_variables": {
                "roll_no": reg_no,
                "class": grade_class,
                "academic_year": academic_year,
                "subjects_table_rows": table_rows_html,
                "cgpa": gpa, # The template uses cgpa, I'll keep the key but value is gpa
                "date_now": date_now
            }
        }

        print(f"Submitting Grade Certificate payload: {payload}")
        backend_url = "http://127.0.0.1:8000/outpass/request_internal"
        
        try:
            response = requests.post(backend_url, json=payload)
            if response.status_code == 200:
                dispatcher.utter_message(template="utter_grade_certificate_submitted")
            else:
                dispatcher.utter_message(text="[ERROR] I couldn't submit your grade certificate request. Please try again later.")
        except Exception as e:
            print(f"Error calling backend: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the system.")

        return [AllSlotsReset()]

class ActionResetGradeSlots(Action):
    def name(self) -> Text:
        return "action_reset_grade_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            SlotSet("grade_first_name", None),
            SlotSet("grade_register_number", None),
            SlotSet("grade_class", None),
            SlotSet("grade_academic_year", None),
            SlotSet("grade_num_subjects", None),
            SlotSet("grade_current_subject_grade", None),
            SlotSet("grade_subjects_grades_list", None),
            SlotSet("grade_subjects_grades", None),
            SlotSet("grade_date", None),
            SlotSet("grade_gpa", None),
            SlotSet("grade_current_index", None)
        ]
