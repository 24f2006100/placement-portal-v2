# Placement Portal Application - V2

## Introduction

The Placement Portal Application is a multi-user web application designed to manage the placement activities of an institute. It provides separate portals for the Admin, Companies, and Students. Companies can create placement drives, students can apply for eligible opportunities, and the Admin can manage the complete placement process. The application also uses Redis caching and Celery for scheduled and asynchronous background jobs.

## Features

- Role-based login and registration for Admin, Students, and Companies.
- Admin can approve companies and placement drives, manage users, and view applications.
- Companies can create placement drives, view applicants, manage application status, and view student resumes.
- Students can search and apply for eligible placement drives, upload resumes, and track their application history.
- Includes daily email reminders, monthly activity reports, CSV exports, and Redis caching.

## Technologies Used

- **Backend:** Flask, Flask-SQLAlchemy
- **Frontend:** Vue.js, Vite, CSS
- **Database:** SQLite
- **Authentication:** JWT
- **Caching:** Redis / Memurai
- **Background Jobs:** Celery and Celery Beat
- **Email Service:** Gmail SMTP

# Installation and Setup

## 1. Clone the Repository

Open a terminal and run:

```bash
git clone YOUR_PRIVATE_REPOSITORY_URL
```

Move into the project directory:

```bash
cd Placement-Portal-V2
```

---

## 2. Create a Python Virtual Environment

Run:

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
venv\Scripts\activate
```

After activation, the terminal should show `(venv)`.

---

## 3. Install Python Dependencies

From the project root directory, run:

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Inside the `backend` folder, create a file named:

```text
.env
```

Add the following:

```env
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

Replace the placeholder values with your own secret keys.

Example:

```env
SECRET_KEY=my_flask_secret_key
JWT_SECRET_KEY=my_jwt_secret_key
```

The `.env` file is ignored by Git and must be created manually after cloning the repository.

---

## 5. Configure Email for Scheduled Jobs

Open:

```text
backend/mail.py
```

Replace:

```python
EMAIL_ADDRESS = "SENDERS_EMAIL"
EMAIL_PASSWORD = "16_CHARACTER_APP_PASSWORD"
```

with the Gmail account that will send the reminder and report emails:

```python
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_16_character_app_password"
```

The email password must be a **Google App Password**, not the normal Gmail account password.

To use a Google App Password:

1. Enable 2-Step Verification on the Google account.
2. Open the Google Account security settings.
3. Create an App Password.
4. Copy the generated 16-character password.
5. Add it to `backend/mail.py`.

---

## 6. Install Node.js and npm

Install Node.js from:

https://nodejs.org/

Verify the installation:

```bash
node --version
```

```bash
npm --version
```

---

## 7. Install Frontend Dependencies

Open a terminal and move into the frontend directory:

```bash
cd frontend
```

Install the required packages:

```bash
npm install
```

---

## 8. Install Redis

The application requires a Redis-compatible server for caching and Celery.

### Windows

This project was developed and tested using **Memurai**, a Redis-compatible server for Windows.

Install Memurai and make sure the Memurai service is running.

To verify that Memurai is running, open PowerShell and run:

```powershell
& "C:\Program Files\Memurai\memurai-cli.exe" ping
```

If Redis/Memurai is working correctly, the output should be:

```text
PONG
```

If Memurai is installed as a Windows service and is already running, it does not need to be started manually every time.

---

# Running the Application

The application requires the Flask backend, Vue frontend, Celery worker, Celery Beat, and Redis/Memurai.

Use separate terminals for the following processes.

---

## Terminal 1 - Run the Flask Backend

Open a terminal in the project root and activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Move into the backend directory:

```bash
cd backend
```

Run:

```bash
python app.py
```

The Flask backend will run at:

```text
http://127.0.0.1:5000
```

On the first run, the SQLite database and default Admin account are created programmatically.

---

## Terminal 2 - Run the Vue Frontend

Open another terminal and move into the frontend directory:

```bash
cd frontend
```

Run:

```bash
npm run dev
```

Open the URL displayed by Vite in the terminal, usually:

```text
http://localhost:5173
```

---

## Terminal 3 - Run the Celery Worker

Open another terminal in the project root and activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Move into the backend directory:

```bash
cd backend
```

Run the Celery worker:

```bash
celery -A celery_app.celery worker --loglevel=info --pool=solo
```

The `--pool=solo` option is used for running Celery on Windows.

---

## Terminal 4 - Run Celery Beat

Open another terminal in the project root and activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Move into the backend directory:

```bash
cd backend
```

Run Celery Beat:

```bash
celery -A celery_app.celery beat --loglevel=info
```

Celery Beat handles the scheduled background jobs.

---

## Redis / Memurai

Redis or Memurai must be running before using caching or Celery background jobs.

Verify it using:

```powershell
& "C:\Program Files\Memurai\memurai-cli.exe" ping
```

Expected output:

```text
PONG
```

---

# Default Admin Login

The Admin account is created programmatically when the application is run for the first time.

Use the Admin credentials configured in:

```text
backend/app.py
```

Default credentials:

```text
Email: admin@portal.com
Password: admin123
```

The application supports only one Admin account, and there is no Admin registration page.

---

# Notes

- Redis/Memurai must be running for caching and Celery tasks.
- The Celery worker must be running for asynchronous jobs.
- Celery Beat must be running for scheduled jobs.
- The sender Gmail account must use a Google App Password for email functionality.
- The `.env` file is not included in the repository and must be created manually.
- The SQLite database is created automatically when the backend is run for the first time.
- Uploaded resumes and generated CSV files are created during application usage and are not stored in the repository.