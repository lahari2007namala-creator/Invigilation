#!/usr/bin/env python
"""
Run this script ONCE after setting up the project to:
1. Apply migrations
2. Create superuser (admin)
3. Add demo data (departments, faculty, rooms, exams)

Usage:
    python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invigilation.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run migrations first
print("Running migrations...")
os.system(f"{sys.executable} manage.py migrate")

django.setup()

from django.contrib.auth.models import User
from exam_system.models import Department, Faculty, ExamRoom, Exam, RoomAllocation
import datetime

print("\n=== Setting up Examination Invigilation System ===\n")

# 1. Create admin user
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@college.edu', 'admin123')
    admin.first_name = 'System'
    admin.last_name = 'Administrator'
    admin.save()
    print("✓ Admin user created  →  username: admin  |  password: admin123")
else:
    print("✓ Admin user already exists")

# 2. Departments
dept_data = [
    ('Computer Science & Engineering', 'CSE'),
    ('Electronics & Communication', 'ECE'),
    ('Mechanical Engineering', 'MECH'),
    ('Civil Engineering', 'CIVIL'),
    ('Information Technology', 'IT'),
]
depts = {}
for name, code in dept_data:
    d, created = Department.objects.get_or_create(code=code, defaults={'name': name})
    depts[code] = d
    if created:
        print(f"✓ Department created: {name}")

# 3. Faculty
faculty_data = [
    ('F001', 'Dr. Rajesh Kumar', 'rajesh@college.edu', '9876543210', 'CSE', 'Professor'),
    ('F002', 'Dr. Priya Sharma', 'priya@college.edu', '9876543211', 'ECE', 'Associate Professor'),
    ('F003', 'Mr. Arun Reddy', 'arun@college.edu', '9876543212', 'MECH', 'Assistant Professor'),
    ('F004', 'Dr. Lakshmi Devi', 'lakshmi@college.edu', '9876543213', 'CIVIL', 'Professor'),
    ('F005', 'Ms. Sneha Patel', 'sneha@college.edu', '9876543214', 'IT', 'Assistant Professor'),
    ('F006', 'Dr. Venkat Rao', 'venkat@college.edu', '9876543215', 'CSE', 'Associate Professor'),
    ('F007', 'Mr. Suresh Babu', 'suresh@college.edu', '9876543216', 'ECE', 'Assistant Professor'),
    ('F008', 'Dr. Meena Iyer', 'meena@college.edu', '9876543217', 'IT', 'Professor'),
]
faculty_users = {}
for eid, name, email, phone, dept_code, desig in faculty_data:
    if not Faculty.objects.filter(employee_id=eid).exists():
        username = eid.lower()
        user = User.objects.create_user(username, email, 'faculty123')
        user.first_name = name.split()[0] if name.startswith('Dr.') or name.startswith('Mr.') or name.startswith('Ms.') else name
        user.save()
        f = Faculty.objects.create(
            user=user, employee_id=eid, name=name, email=email,
            phone=phone, department=depts[dept_code], designation=desig
        )
        faculty_users[eid] = f
        print(f"✓ Faculty created: {name}  →  username: {username}  |  password: faculty123")
    else:
        faculty_users[eid] = Faculty.objects.get(employee_id=eid)

# 4. Rooms
room_data = [
    ('101', 'Main Block', 60, 1),
    ('102', 'Main Block', 60, 1),
    ('201', 'Main Block', 80, 2),
    ('202', 'Main Block', 80, 2),
    ('LAB-A', 'Lab Block', 40, 1),
    ('LAB-B', 'Lab Block', 40, 1),
    ('HALL-1', 'Exam Hall', 150, 0),
]
rooms = {}
for rno, bldg, cap, floor in room_data:
    r, created = ExamRoom.objects.get_or_create(room_number=rno, defaults={'building': bldg, 'capacity': cap, 'floor': floor})
    rooms[rno] = r
    if created:
        print(f"✓ Room created: Room {rno}, {bldg}")

# 5. Exams
today = datetime.date.today()
exam_data = [
    ('Data Structures', 'CS301', 'CSE', 3, today + datetime.timedelta(days=5)),
    ('Digital Electronics', 'EC201', 'ECE', 2, today + datetime.timedelta(days=7)),
    ('Engineering Mathematics', 'MA101', 'CSE', 1, today + datetime.timedelta(days=10)),
    ('Database Management', 'CS401', 'CSE', 4, today + datetime.timedelta(days=3)),
    ('Computer Networks', 'CS501', 'IT', 5, today + datetime.timedelta(days=12)),
]
for sname, scode, dept_code, sem, edate in exam_data:
    exam, created = Exam.objects.get_or_create(
        subject_code=scode,
        defaults={
            'subject_name': sname, 'department': depts[dept_code],
            'semester': sem, 'exam_date': edate,
            'start_time': datetime.time(9, 0), 'end_time': datetime.time(12, 0),
            'total_students': 60, 'status': 'upcoming'
        }
    )
    if created:
        RoomAllocation.objects.get_or_create(exam=exam, room=rooms['101'], defaults={'students_count': 30})
        RoomAllocation.objects.get_or_create(exam=exam, room=rooms['102'], defaults={'students_count': 30})
        print(f"✓ Exam created: {sname} on {edate}")

print("\n" + "="*50)
print("✅ Setup complete! Run the server with:")
print("   python manage.py runserver")
print("\n🔑 Admin Login:   username=admin      password=admin123")
print("🎓 Faculty Login: username=f001..f008  password=faculty123")
print("🌐 URL: http://127.0.0.1:8000/")
print("="*50 + "\n")
