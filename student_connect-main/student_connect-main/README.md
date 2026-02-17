# CampusConnect: AI-Powered Student Management Ecosystem

CampusConnect is a professional-grade student management system featuring an AI Assistant for automated outpass/certificate issuance, a premium Admin Dashboard, and a modern Flutter mobile application.

## 🚀 Project Architecture

The project is divided into three main components:
1.  **Backend (`/back`)**: Flask API integrated with Rasa NLP for conversational intelligence.
2.  **Admin Dashboard (`/admin_dashboard`)**: React (Vite) application for institutional oversight.
3.  **Student App (`/student_connect_fixed`)**: Cross-platform Flutter app for student interactions.

---

## 🛠 Prerequisites

Before starting, ensure you have the following installed:
*   **Flutter SDK**: (v3.19+ recommended)
*   **Node.js & npm**: (v18+ recommended)
*   **Python**: 3.10.x (Specific version required for Rasa)
*   **MongoDB**: Local or Atlas instance.

---

## 💻 Setup Instructions

### 1. Backend & AI Assistant (`/back`)
The backend uses two separate virtual environments to ensure compatibility between Flask and Rasa.

```bash
cd back

# Setup Flask Virtual Environment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Setup Rasa Virtual Environment
python -m venv venv_rasa
.\venv_rasa\Scripts\activate
pip install rasa rasa-sdk requests xhtml2pdf
```

**Running the Backend:**
Open 3 separate terminals in the `back` directory:
*   **Term 1 (Flask)**: `.\venv\Scripts\activate; python app.py`
*   **Term 2 (Rasa Actions)**: `.\venv_rasa\Scripts\activate; cd rasa; rasa run actions`
*   **Term 3 (Rasa Server)**: `.\venv_rasa\Scripts\activate; cd rasa; rasa run --enable-api --cors "*"`

### 2. Admin Dashboard (`/admin_dashboard`)
```bash
cd admin_dashboard
npm install
npm run dev
```
The dashboard will be available at `http://localhost:5173`.

### 3. Student Mobile App (`/student_connect_fixed`)
```bash
cd student_connect_fixed
flutter pub get
flutter run
```

---

## ✨ Key Features

### 🤖 AI-Powered Outpass System
*   **Conversational Logic**: Students can apply for outpasses by talking to the AI.
*   **Status Tracking**: Ask the AI *"What is my status?"* for a real-time tracking list.
*   **Smart Issuance**: If approved, the AI sends a professional PDF Document Card.

### 📄 Professional Document Generation
*   **Master Templates**: Administrators design outpass/certificate templates in the dashboard.
*   **Automatic Attachment**: The system dynamically injects student details (Roll No, Dept, Reason) into the template upon approval.
*   **Native PDF**: Uses `xhtml2pdf` to generate official binary PDF files viewable on any device.

### 📱 Premium Student UX
*   **Persistent Sessions**: Sign in once; stay logged in across sessions using `shared_preferences`.
*   **Global Status Center**: Dedicated section to track all active and past applications with color-coded status indicators.
*   **Academic Tracker**: View course progress and curriculum snapshots.

---

## 📝 Important Configuration
*   **Backend URL**: Ensure the `baseUrl` in `student_connect_fixed/lib/config.dart` matches your local machine's IP (use `10.0.2.2` for Android Emulator).
*   **NDK Version**: This project requires Android **NDK 27.0.12077973**. I have pre-configured this in `build.gradle.kts`.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
