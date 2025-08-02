## QuickDesk

A modern, role-based support ticketing platform for organizations. QuickDesk lets users (employees) create support tickets, while agents and admins manage and resolve them through a streamlined dashboard.

---

## Purpose 

The purpose of QuickDesk is to provide a simple, easy-to-use help desk solution
where users can raise support tickets, and support staff can manage and resolve
them efficiently. The system aims to streamline communication between users
and support teams without unnecessary complexity

---

## Snapshots

Find video here: https://drive.google.com/drive/folders/1D15lU-UeEJDm_eVxiCsQSD4knRSrO9aX

<img width="1365" height="616" alt="image" src="https://github.com/user-attachments/assets/cc15ab9c-03df-4655-a8c0-6780c80b5059" />

<img width="1356" height="610" alt="image" src="https://github.com/user-attachments/assets/51f68ebc-c114-42c4-ba8c-831ff725894d" />

<img width="1352" height="616" alt="image" src="https://github.com/user-attachments/assets/72fd5a90-4638-43a5-9b24-3a168d615245" />

<img width="1365" height="624" alt="image" src="https://github.com/user-attachments/assets/f1863e70-41bb-4cf5-9e85-6fe0a957cb7f" />

<img width="1359" height="619" alt="image" src="https://github.com/user-attachments/assets/6edb5326-6895-4841-a05e-894691dd3d99" />

<img width="1342" height="624" alt="image" src="https://github.com/user-attachments/assets/8c426d06-baa8-4432-8bc6-098d41c86252" />

<img width="1339" height="444" alt="image" src="https://github.com/user-attachments/assets/3bcb0661-7622-4c97-a75d-1f5f7e1aed8d" />

<img width="1346" height="625" alt="image" src="https://github.com/user-attachments/assets/172252cb-e577-47c6-bf47-54223eddfa09" />

<img width="1344" height="625" alt="image" src="https://github.com/user-attachments/assets/21d93848-334e-47be-a7d7-2ddb133f839d" />

<img width="1340" height="622" alt="image" src="https://github.com/user-attachments/assets/4c12c64e-10ce-46ce-ba08-f1c22eafdb9a" />

<img width="1363" height="614" alt="image" src="https://github.com/user-attachments/assets/146d0a6d-e636-4995-a943-ccacfbbeb878" />

<img width="1364" height="631" alt="image" src="https://github.com/user-attachments/assets/30f8c3a6-abb1-4a2f-afd4-74f09361d717" />

<img width="1362" height="610" alt="image" src="https://github.com/user-attachments/assets/4f164c1a-4459-4c62-bc64-e85fcdbfd14f" />




---

## Architecture

<img width="661" height="493" alt="Untitled Diagram drawio (3)" src="https://github.com/user-attachments/assets/a034bf29-5a9c-4b60-a1ec-636f98f3c0c9" />

--- 

## Users

- End Users (Employees/Customers): Can create and track their tickets.
- Support Agents: Can respond to and resolve tickets.
- Admin: Can manage users, categories, and overall ticket flow

---

## 🧠 Overview

**QuickDesk** is a Flask-powered support system that:
- Allows users to raise support tickets with attachments.
- Enables agents to manage tickets assigned to them.
- Lets admins monitor all tickets, users, and categories.
- Provides real-time email notifications for updates.
- Includes upvote/downvote feedback on tickets.
- Role-based access and personalized dashboards.
- Features full search, filter, and status tracking.
- AI-Powered Automation
- Auto-Closure of Invalid Tickets

Tickets with inappropriate language are immediately auto-closed.
Tickets with gibberish or irrelevant content (like "asdf", "hi", "test") are auto-rejected.
Admins and agents are notified of such tickets.
This smart handling ensures cleaner ticket queues and faster resolution cycles.

---

## 🔧 Tech Stack

| Layer       | Technology         |
|------------|--------------------|
| Backend     | Python (Flask)     |
| Frontend    | HTML, Jinja2, Bootstrap 5 |
| Database    | SQLite (default) / PostgreSQL / MySQL (optional) |
| ORM         | SQLAlchemy         |
| Email       | Flask-Mail (Gmail SMTP) |
| Session/Auth| Flask-Login        |
| File Upload | Werkzeug + Flask   |

---

## 📦 Python Dependencies

```
Flask==2.3.2
Flask-Login==0.6.2
Flask-Mail==0.9.1
Flask-SQLAlchemy==3.0.5
```

---

## 📁 Project Structure

```
quickdesk/
├── app.py
├── models.py
├── forms.py
├── routes/
│   ├── auth.py
│   ├── tickets.py
│   ├── agent.py
│   └── admin.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── profile.html
│   └── ...
├── static/
│   ├── style.css
│   └── uploads/
├── utils/
│   ├── email_utils.py
│   └── filters.py
├── config.py
├── run.py
└── README.md
```

---

## 🏗️ Setup Instructions

### 1. 🔃 Clone the Repo

```bash
git clone https://github.com/vaibhavrawat27/quickdesk.git
cd quickdesk
```

### 3. 🧩 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🔐 Set up MAIL Passowrd for email notification system

```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 5. 🗃️ Initialize the Database

```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 6. 🚀 Run the App

```bash
flask run
```

Then visit: `http://127.0.0.1:5000/`

---

## 🧪 How It Works

### Roles
- **User**: Creates tickets, views replies, updates profile.
- **Agent**: Views assigned tickets, replies, and updates status.
- **Admin**: Views all tickets, manages users, categories, agents.

### Ticket Lifecycle
```
User → Create Ticket → Assigned to Agent → Agent Responds → Status Updated → Email Notifications
```

<img width="396" height="241" alt="Ticket-LifeCycle" src="https://github.com/user-attachments/assets/5872ea52-0fbd-4f74-a58f-b7e783633f35" />


### Email Notifications
- Sent via `Flask-Mail` on:
  - New ticket submission (to admin and agents)
  - Ticket status updates
  - Replies to tickets

---

## 🧠 Core Features

- ✅ Login/Registration with Flask-Login
- ✅ Role-Based Access Control
- ✅ Ticket Submission with Category & File Upload
- ✅ Agent and Admin Dashboards
- ✅ Upvote/Downvote on Tickets
- ✅ Real-Time Filters (Search, Category, Date, Status)
- ✅ Email Notifications
- ✅ Profile Update & Password Change
- ✅ Delete Account with Password Confirmation

---

## 🧪 Testing Tips

- Test multiple roles with dummy data.
- Attach small images/files for file upload.
- Try creating multiple categories as admin.
- Trigger email logs in console if Gmail SMTP blocks sending.

---

## 📬 Email Setup (Gmail SMTP)

1. Enable **2-Step Verification** for your Gmail account.
2. Generate an **App Password** from Google Account > Security > App Passwords.
3. Add it to your `.env` or make changes in config.

---

## 📌 Future Ideas

- Add analytics dashboard for admins.
- Assign tickets to specific agents automatically.
- Enable comment threads on replies.
- Add real-time notification bell.
- Integrate chat support (via SocketIO or external APIs).

---

## 🙌 Declaration & Acknowledgement 

- I hereby declare that I have completed this project during the Odoo x CGC Hackathon held on 2nd August 2025, within the designated time frame of 9:00 AM to 5:00 PM.
- While I have utilized the internet and AI-based tools for research and reference purposes, I affirm that:
- All work presented is my own.
- I fully understand the code and logic implemented in the project.
- No part of the project was blindly copied or misused.
- This declaration confirms both the originality of my contribution and my understanding of the tools and techniques used.

