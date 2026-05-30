# 📋 Examination Invigilation Duty Allocator
**By:** Lahari (2520090226) & Bhanu Priya (2520090171)

---

## 🚀 Quick Start (3 steps)

### Step 1 — Install Django
```bash
pip install -r requirements.txt
```

### Step 2 — Setup & Demo Data
```bash
python setup.py
```

### Step 3 — Run
```bash
python manage.py runserver
```
Open → **http://127.0.0.1:8000/**

---

## 🔑 Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Faculty | `f001` to `f008` | `faculty123` |

---

## 📦 Modules

| Module | Description |
|--------|-------------|
| **Administration** | Manage faculty, departments, user accounts |
| **Exam Scheduling** | Schedule exams, allocate rooms to exams |
| **Invigilation Duty Assignment** | Manual & auto-assign duties to faculty |
| **Faculty Dashboard & Notifications** | Faculty view duties, receive notifications |

---

## 🗂 Project Structure

```
invigilation/
├── manage.py
├── setup.py          ← Run this first!
├── requirements.txt
├── invigilation/     ← Django project config
│   ├── settings.py
│   └── urls.py
└── exam_system/      ← Main app
    ├── models.py     ← Database models
    ├── views.py      ← All page logic
    ├── forms.py      ← Form definitions
    ├── urls.py       ← URL routes
    ├── admin.py      ← Django admin
    └── templates/    ← HTML pages
```

---

## 🎨 Features
- ✅ Pastel colour scheme (purple, blue, green, pink)
- ✅ Admin & Faculty separate dashboards
- ✅ Smart auto-assign (fair workload distribution)
- ✅ Real-time notifications to faculty
- ✅ CSV export of all duties
- ✅ Search & filter on all pages
- ✅ Room allocation management
- ✅ Reports & analytics page
- ✅ SQLite database (no setup required)
