Write-Host "Starting CampusConnect Project..."

$root = Get-Location

# 1. Start Backend - Flask
Write-Host "Launching Flask Backend..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; .\back\venv\Scripts\python.exe back\app.py"

# 2. Start Backend - Rasa Actions
Write-Host "Launching Rasa Actions..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; .\v\Scripts\python.exe -m rasa_sdk.endpoint --actions back.rasa.actions -p 5055"

# 3. Start Backend - Rasa Server
Write-Host "Launching Rasa Server..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; .\v\Scripts\python.exe -m rasa run --enable-api --cors '*' --model back\rasa\models --endpoints back\rasa\endpoints.yml --credentials back\rasa\credentials.yml"

# 4. Start Admin Dashboard
Write-Host "Launching Admin Dashboard..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\admin_dashboard'; npm run dev"

# 5. Start Student App (Flutter)
Write-Host "Launching Student App..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\student_connect_fixed'; flutter run"

Write-Host "All components have been launched in separate windows."
Write-Host "Note: Rasa may take up to 60 seconds to fully load its AI models."
