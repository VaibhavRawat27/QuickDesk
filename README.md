# 📄 QuickDesk – Ticketing Helpdesk System

A modern, role-based support ticketing platform for organizations. QuickDesk lets users (employees) create support tickets, while agents and admins manage and resolve them through a streamlined dashboard.

---

## Purpose 

The purpose of QuickDesk is to provide a simple, easy-to-use help desk solution
where users can raise support tickets, and support staff can manage and resolve
them efficiently. The system aims to streamline communication between users
and support teams without unnecessary complexity

---

## Architecture

<img width="661" height="493" alt="archiecture" src="https://github.com/user-attachments/assets/85597443-35b4-4abd-ae53-f9feb820ea97" />

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

I have completed this project during odoo x cgc hackathon on 2nd August 2025 during time spam of 9 am to 5 pm.

I acknowledge i have used internet and ai tools, but these tools are only used to do research. I am well aware of all the code i used and know what it work exactly.

