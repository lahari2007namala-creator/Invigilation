from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    duty_count = models.IntegerField(default=0)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Faculty Members'


class ExamRoom(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    building = models.CharField(max_length=100)
    capacity = models.IntegerField()
    floor = models.IntegerField(default=1)

    def __str__(self):
        return f"Room {self.room_number} - {self.building}"

    class Meta:
        ordering = ['room_number']


class Exam(models.Model):
    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    subject_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    total_students = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} - {self.exam_date}"

    class Meta:
        ordering = ['-exam_date']


class RoomAllocation(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='room_allocations')
    room = models.ForeignKey(ExamRoom, on_delete=models.CASCADE)
    students_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('exam', 'room')

    def __str__(self):
        return f"{self.exam.subject_code} - {self.room.room_number}"


class InvigilationDuty(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    ]

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='duties')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='duties')
    room = models.ForeignKey(ExamRoom, on_delete=models.CASCADE)
    duty_date = models.DateField()
    reporting_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    notes = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('faculty', 'exam')
        ordering = ['-duty_date']

    def __str__(self):
        return f"{self.faculty.name} - {self.exam.subject_name} ({self.duty_date})"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('duty_assigned', 'Duty Assigned'),
        ('duty_updated', 'Duty Updated'),
        ('exam_reminder', 'Exam Reminder'),
        ('general', 'General'),
    ]

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty.name} - {self.title}"

    class Meta:
        ordering = ['-created_at']
