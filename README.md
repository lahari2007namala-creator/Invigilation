# Examination Invigilation System — Setup Guide

---

## Step 1 — Install Python

1. Go to **https://www.python.org/downloads/**
2. Click **Download Python 3.12.x**
3. Run the installer
4. ✅ Check **"Add Python to PATH"** at the bottom
5. Click **Install Now**

---

## Step 2 — Download the Project

```cmd
cd Downloads
git clone https://github.com/lahari2007namala-creator/Invigilation.git
cd Invigilation
```

> Or download the ZIP from GitHub and extract it, then open Command Prompt inside the folder.

---

## Step 3 — Install Django

```cmd
py -m pip install django
```

> This installs Django, the framework the project is built on.

---

## Step 4 — Run These 4 Commands

```cmd
py manage.py makemigrations exam_system
py manage.py migrate
py setup.py
py manage.py runserver
```

### What each command does:

| Command | What it does |
|---|---|
| `makemigrations exam_system` | Reads the database models and prepares the table creation instructions |
| `migrate` | Actually creates all the database tables |
| `setup.py` | Fills the database with demo data (admin user, faculty, exams, etc.) |
| `runserver` | Starts the website on your computer |

---

## Step 5 — Open in Browser

Go to **http://127.0.0.1:8000/**

### Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Faculty | `f001` to `f008` | `faculty123` |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `py` not recognized | Reinstall Python and check "Add to PATH" |
| `No module named django` | Run `py -m pip install django` again |
| `no such table` error | Run `makemigrations` and `migrate` again |
| Port already in use | Run `py manage.py runserver 8080` and open `http://127.0.0.1:8080/` |
