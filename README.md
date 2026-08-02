# DevBoard Pro — Smart Project & Task Management System

A full-stack project & task management web app built with **Flask, SQLAlchemy, Flask-Login, Flask-WTF, Bootstrap 5, and Chart.js**.

## Features
- Register / Login / Logout with hashed passwords (Werkzeug)
- Dashboard with live stat cards + Chart.js charts (status, priority, completion %)
- Project CRUD + search
- Task CRUD + search, status (To Do / In Progress / Completed), priority (High/Medium/Low), due dates
- Overdue task detection
- Profile update + change password
- CSV export of tasks
- Dark mode toggle (persisted via localStorage)
- Responsive Bootstrap 5 UI, custom-styled

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python run.py
```

Visit **http://127.0.0.1:5000**

## Project Structure

```
devboard-pro/
├── app/
│   ├── models/        # User, Project, Task (SQLAlchemy)
│   ├── routes/         # Blueprints: main, auth, dashboard, projects, tasks, profile
│   ├── forms/          # Flask-WTF forms
│   ├── templates/      # Jinja2 templates (Bootstrap 5)
│   ├── static/          # css/js
│   └── extensions.py    # db, login_manager singletons
├── instance/            # SQLite database created here at runtime
├── run.py
├── requirements.txt
└── .env
```

## Tech Stack
- **Backend:** Python, Flask, SQLAlchemy, Flask-Login, Flask-WTF, Werkzeug
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript, Bootstrap Icons, Chart.js
- **Database:** SQLite
