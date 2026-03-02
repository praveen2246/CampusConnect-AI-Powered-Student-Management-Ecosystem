# CampusConnect: AI-Powered Student Management Ecosystem

CampusConnect is a professional-grade student management system featuring an AI Assistant for automated outpass/certificate issuance, a premium Admin Dashboard, and a modern Flutter mobile application.

---

## 📂 Project Structure

```bash
student_connect-main/
├── back/                   # Python Flask Backend
│   ├── rasa/               # Rasa NLU & Custom Actions
│   ├── routes/             # API Endpoints
│   ├── admin.py            # Admin Dashboard Logic
│   ├── app.py              # Main Application Entry
│   ├── db.py               # MongoDB Configuration
│   ├── seed_template.py    # Official Document HTML Templates
│   └── venv/               # Flask Virtual Environment
├── admin_dashboard/        # React + Vite Frontend
│   └── src/
│       ├── pages/          # Admin UI Modules
│       └── services/       # API Integration
├── student_connect_fixed/   # Flutter Mobile Application
│   └── lib/                # Dart Frontend Logic
├── v/                      # Rasa Virtual Environment
└── run_project.ps1         # Unified Startup Script
```

---

## 🛠 Prerequisites

Ensure you have the following installed:
*   **Flutter SDK**: v3.19+
*   **Node.js & npm**: v18+
*   **Python**: 3.10.x (Critical for Rasa compatibility)
*   **MongoDB**: Local instance running on port `27017`

---

## 💻 Setup Instructions

### 1. Backend & AI Assistant (`/back`)
The project utilizes environment isolation between the core API and the NLP engine.

```bash
# Setup Flask Environment
cd back
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Setup Rasa Environment (in root)
cd ..
python -m venv v
.\v\Scripts\activate
pip install rasa rasa-sdk requests xhtml2pdf pymongo python-dotenv
```

### 2. Admin Dashboard (`/admin_dashboard`)
```bash
cd admin_dashboard
npm install
```

### 3. Student Mobile App (`/student_connect_fixed`)
```bash
cd student_connect_fixed
flutter pub get
```

---

## 🚀 Running the Project

### Automatic Option (Recommended)
Run the following from the root directory to start all services:
```powershell
./run_project.ps1
```

### Manual Option
Open 4 separate terminals:
1.  **Flask API**: `cd back; .\venv\Scripts\activate; python app.py`
2.  **Rasa Actions**: `cd back\rasa; ..\..\v\Scripts\activate; rasa run actions`
3.  **Rasa Server**: `cd back\rasa; ..\..\v\Scripts\activate; rasa run --enable-api --cors "*"`
4.  **Admin Dashboard**: `cd admin_dashboard; npm run dev`

---

## ✨ Key Features

### 🤖 AI-Powered Document Flow
*   **Outpass Generation**: conversational logic for leave requests.
*   **Bonafide Certificates**: automated verification and issuance.
*   **Grade Certificates / Marksheets**: Integrated flow to capture student details and generate GPA summaries.

### 📄 Professional PDF Generation
*   **Dynamic Templating**: Uses `xhtml2pdf` to convert HTML/CSS into premium binary PDFs.
*   **Institutional Identity**: Automated injection of college names, signatures, and stamps.
*   **One-Page Layout**: Optimized CSS ensures all certificates fit perfectly on a single A4 page.

### 📱 Premium Student UX
*   **Persistent Sessions**: secure authentication using JWT.
*   **Real-time Tracking**: Dedicated status center to monitor pending, approved, and rejected applications.
*   **Digital Downloads**: In-app PDF viewer for instant document access.

---

## 📝 Important Configuration

*   **Fixed IPs**: If running on mobile, update `baseUrl` in `lib/config.dart` to your machine's local IP (e.g., `192.168.x.x`).
*   **Database**: Ensure `MONGO_DB_NAME` in `.env` matches your intended database name (default: `college_chatbot`).
*   **PDF Fixes**: If certificates crash on download, ensure the template height properties are removed from `seed_template.py`.

---

## 📄 License
This project is licensed under the MIT License.
