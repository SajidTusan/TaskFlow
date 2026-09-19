# TaskFlow - Task & Productivity Management Web App

TaskFlow is a robust, full-stack Django web application designed to help users manage their daily tasks, set priorities, track due dates, and organize activities by categories efficiently. Built with clean architecture, custom user authentication, and fully configured for cloud deployment on Render with PostgreSQL.

---

## 🚀 Features

* **User Authentication System:** Secure registration, login, and logout capabilities.
* **Task Management (CRUD):** Create, view, update, and delete tasks with ease.
* **Categorization & Priorities:** Assign categories and priority levels (High, Medium, Low) to structure work.
* **Due Date Tracking:** Set target completion dates for time-sensitive tasks.
* **User Isolation:** Each user has private access exclusively to their own tasks and categories.
* **Responsive UI:** Styled layout with custom CSS for smooth desktop and mobile experience.
* **Automated Admin Setup:** Configured script to auto-provision superuser credentials upon deployment.
* **Production Ready:** Configured for PostgreSQL integration and dynamic static file serving via `gunicorn`.

---

## 🛠️ Tech Stack

* **Backend Framework:** Django 5+ / Python 3.12+
* **Database:** SQLite (Local Development) / PostgreSQL (Production)
* **Frontend:** HTML5, CSS3, Django Templates
* **Production Server:** Gunicorn
* **Database Adapter:** `psycopg[binary]`
* **Version Control & Hosting:** Git, GitHub, Render

---

## 📁 Project Structure

```text
TaskFlow/
│
├── config/                 # Project configuration root
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # App settings & env configuration
│   ├── urls.py             # Global URL routing
│   └── wsgi.py             # WSGI entry point for deployment
│
├── tasks/                  # Task application logic
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates for tasks & auth
│   ├── admin.py            # Django Admin registration
│   ├── apps.py
│   ├── forms.py            # Django forms for tasks
│   ├── models.py           # Database schemas (Task, Category)
│   ├── urls.py             # Task app routes
│   └── views.py            # Application logic & controllers
│
├── static/                 # Static assets (CSS, JS, Images)
│   └── css/
│       └── style.css
│
├── .gitignore              # Ignored files (venv, db.sqlite3, staticfiles)
├── build.sh                # Automated build script for Render deployment
├── manage.py               # Django management CLI
├── README.md               # Project documentation
└── requirements.txt        # Python package dependencies
