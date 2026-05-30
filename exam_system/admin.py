from django.contrib import admin
from .models import Faculty, Exam, ExamRoom, RoomAllocation, InvigilationDuty, Department, Notification


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'employee_id', 'department', 'designation', 'duty_count', 'is_available']
    list_filter = ['department', 'is_available']
    search_fields = ['name', 'employee_id', 'email']


@admin.register(ExamRoom)
class ExamRoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'building', 'floor', 'capacity']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'subject_code', 'department', 'semester', 'exam_date', 'status']
    list_filter = ['status', 'department', 'semester']
    search_fields = ['subject_name', 'subject_code']


@admin.register(RoomAllocation)
class RoomAllocationAdmin(admin.ModelAdmin):
    list_display = ['exam', 'room', 'students_count']


@admin.register(InvigilationDuty)
class InvigilationDutyAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'exam', 'room', 'duty_date', 'status']
    list_filter = ['status', 'duty_date']
    search_fields = ['faculty__name', 'exam__subject_name']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
