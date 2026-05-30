from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse
from django.utils import timezone
import csv, datetime

from .models import Faculty, Exam, ExamRoom, RoomAllocation, InvigilationDuty, Department, Notification
from .forms import (LoginForm, FacultyForm, ExamForm, ExamRoomForm,
                    RoomAllocationForm, InvigilationDutyForm, DepartmentForm, NotificationForm)


def is_admin(user):
    return user.is_staff or user.is_superuser


# ─── AUTH ───────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
        return redirect('dashboard')
    return render(request, 'exam_system/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─── DASHBOARD ──────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    if is_admin(request.user):
        # Admin dashboard
        today = timezone.now().date()
        context = {
            'total_faculty': Faculty.objects.count(),
            'total_exams': Exam.objects.count(),
            'total_rooms': ExamRoom.objects.count(),
            'total_duties': InvigilationDuty.objects.count(),
            'upcoming_exams': Exam.objects.filter(status='upcoming').order_by('exam_date')[:5],
            'recent_duties': InvigilationDuty.objects.order_by('-assigned_at')[:5],
            'today_exams': Exam.objects.filter(exam_date=today),
            'unread_notifications': Notification.objects.filter(is_read=False).count(),
            'is_admin': True,
        }
        return render(request, 'exam_system/admin_dashboard.html', context)
    else:
        # Faculty dashboard
        try:
            faculty = Faculty.objects.get(user=request.user)
            duties = InvigilationDuty.objects.filter(faculty=faculty).order_by('duty_date')
            notifications = Notification.objects.filter(faculty=faculty, is_read=False)[:5]
            upcoming = duties.filter(status__in=['assigned', 'confirmed']).filter(duty_date__gte=timezone.now().date())
            context = {
                'faculty': faculty,
                'duties': duties[:10],
                'upcoming_duties': upcoming,
                'notifications': notifications,
                'unread_count': Notification.objects.filter(faculty=faculty, is_read=False).count(),
                'total_duties': duties.count(),
                'completed_duties': duties.filter(status='completed').count(),
                'is_admin': False,
            }
        except Faculty.DoesNotExist:
            context = {'no_profile': True, 'is_admin': False}
        return render(request, 'exam_system/faculty_dashboard.html', context)


# ─── FACULTY MANAGEMENT ─────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def faculty_list(request):
    q = request.GET.get('q', '')
    dept = request.GET.get('dept', '')
    faculty = Faculty.objects.select_related('department')
    if q:
        faculty = faculty.filter(Q(name__icontains=q) | Q(employee_id__icontains=q) | Q(email__icontains=q))
    if dept:
        faculty = faculty.filter(department__id=dept)
    return render(request, 'exam_system/faculty_list.html', {
        'faculty_list': faculty,
        'departments': Department.objects.all(),
        'search': q,
        'selected_dept': dept,
    })


@login_required
@user_passes_test(is_admin)
def faculty_add(request):
    form = FacultyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Faculty member added successfully!')
        return redirect('faculty_list')
    return render(request, 'exam_system/faculty_form.html', {'form': form, 'title': 'Add Faculty'})


@login_required
@user_passes_test(is_admin)
def faculty_edit(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    form = FacultyForm(request.POST or None, instance=faculty)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Faculty updated successfully!')
        return redirect('faculty_list')
    return render(request, 'exam_system/faculty_form.html', {'form': form, 'title': 'Edit Faculty', 'obj': faculty})


@login_required
@user_passes_test(is_admin)
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        faculty.delete()
        messages.success(request, 'Faculty member removed.')
        return redirect('faculty_list')
    return render(request, 'exam_system/confirm_delete.html', {'obj': faculty, 'type': 'Faculty Member'})


@login_required
@user_passes_test(is_admin)
def faculty_detail(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    duties = InvigilationDuty.objects.filter(faculty=faculty).order_by('-duty_date')
    return render(request, 'exam_system/faculty_detail.html', {'faculty': faculty, 'duties': duties})


# ─── EXAM SCHEDULING ────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def exam_list(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    exams = Exam.objects.select_related('department')
    if q:
        exams = exams.filter(Q(subject_name__icontains=q) | Q(subject_code__icontains=q))
    if status:
        exams = exams.filter(status=status)
    return render(request, 'exam_system/exam_list.html', {
        'exams': exams,
        'search': q,
        'selected_status': status,
    })


@login_required
@user_passes_test(is_admin)
def exam_add(request):
    form = ExamForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Exam scheduled successfully!')
        return redirect('exam_list')
    return render(request, 'exam_system/exam_form.html', {'form': form, 'title': 'Schedule Exam'})


@login_required
@user_passes_test(is_admin)
def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    form = ExamForm(request.POST or None, instance=exam)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Exam updated successfully!')
        return redirect('exam_list')
    return render(request, 'exam_system/exam_form.html', {'form': form, 'title': 'Edit Exam', 'obj': exam})


@login_required
@user_passes_test(is_admin)
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam removed.')
        return redirect('exam_list')
    return render(request, 'exam_system/confirm_delete.html', {'obj': exam, 'type': 'Exam'})


# ─── ROOM MANAGEMENT ────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def room_list(request):
    rooms = ExamRoom.objects.all()
    return render(request, 'exam_system/room_list.html', {'rooms': rooms})


@login_required
@user_passes_test(is_admin)
def room_add(request):
    form = ExamRoomForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Room added successfully!')
        return redirect('room_list')
    return render(request, 'exam_system/room_form.html', {'form': form, 'title': 'Add Room'})


@login_required
@user_passes_test(is_admin)
def room_edit(request, pk):
    room = get_object_or_404(ExamRoom, pk=pk)
    form = ExamRoomForm(request.POST or None, instance=room)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Room updated!')
        return redirect('room_list')
    return render(request, 'exam_system/room_form.html', {'form': form, 'title': 'Edit Room', 'obj': room})


@login_required
@user_passes_test(is_admin)
def room_delete(request, pk):
    room = get_object_or_404(ExamRoom, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room removed.')
        return redirect('room_list')
    return render(request, 'exam_system/confirm_delete.html', {'obj': room, 'type': 'Room'})


# ─── ROOM ALLOCATION ────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def allocation_list(request):
    allocations = RoomAllocation.objects.select_related('exam', 'room').order_by('-exam__exam_date')
    return render(request, 'exam_system/allocation_list.html', {'allocations': allocations})


@login_required
@user_passes_test(is_admin)
def allocation_add(request):
    form = RoomAllocationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Room allocated successfully!')
        return redirect('allocation_list')
    return render(request, 'exam_system/allocation_form.html', {'form': form, 'title': 'Allocate Room'})


@login_required
@user_passes_test(is_admin)
def allocation_delete(request, pk):
    alloc = get_object_or_404(RoomAllocation, pk=pk)
    if request.method == 'POST':
        alloc.delete()
        messages.success(request, 'Allocation removed.')
        return redirect('allocation_list')
    return render(request, 'exam_system/confirm_delete.html', {'obj': alloc, 'type': 'Room Allocation'})


# ─── INVIGILATION DUTIES ────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def duty_list(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    duties = InvigilationDuty.objects.select_related('faculty', 'exam', 'room')
    if q:
        duties = duties.filter(Q(faculty__name__icontains=q) | Q(exam__subject_name__icontains=q))
    if status:
        duties = duties.filter(status=status)
    return render(request, 'exam_system/duty_list.html', {
        'duties': duties,
        'search': q,
        'selected_status': status,
    })


@login_required
@user_passes_test(is_admin)
def duty_add(request):
    form = InvigilationDutyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        duty = form.save()
        # Update duty count
        duty.faculty.duty_count += 1
        duty.faculty.save()
        # Send notification
        Notification.objects.create(
            faculty=duty.faculty,
            title='New Invigilation Duty Assigned',
            message=f'You have been assigned invigilation duty for {duty.exam.subject_name} on {duty.duty_date} at {duty.reporting_time} in Room {duty.room.room_number}.',
            notification_type='duty_assigned'
        )
        messages.success(request, 'Duty assigned and faculty notified!')
        return redirect('duty_list')
    return render(request, 'exam_system/duty_form.html', {'form': form, 'title': 'Assign Duty'})


@login_required
@user_passes_test(is_admin)
def duty_edit(request, pk):
    duty = get_object_or_404(InvigilationDuty, pk=pk)
    form = InvigilationDutyForm(request.POST or None, instance=duty)
    if request.method == 'POST' and form.is_valid():
        form.save()
        Notification.objects.create(
            faculty=duty.faculty,
            title='Invigilation Duty Updated',
            message=f'Your duty for {duty.exam.subject_name} on {duty.duty_date} has been updated.',
            notification_type='duty_updated'
        )
        messages.success(request, 'Duty updated and faculty notified!')
        return redirect('duty_list')
    return render(request, 'exam_system/duty_form.html', {'form': form, 'title': 'Edit Duty', 'obj': duty})


@login_required
@user_passes_test(is_admin)
def duty_delete(request, pk):
    duty = get_object_or_404(InvigilationDuty, pk=pk)
    if request.method == 'POST':
        if duty.faculty.duty_count > 0:
            duty.faculty.duty_count -= 1
            duty.faculty.save()
        duty.delete()
        messages.success(request, 'Duty removed.')
        return redirect('duty_list')
    return render(request, 'exam_system/confirm_delete.html', {'obj': duty, 'type': 'Invigilation Duty'})


@login_required
@user_passes_test(is_admin)
def auto_assign_duties(request):
    """Auto assign duties fairly based on duty_count"""
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        exam = get_object_or_404(Exam, pk=exam_id)
        allocations = RoomAllocation.objects.filter(exam=exam)
        available_faculty = Faculty.objects.filter(is_available=True).order_by('duty_count')
        assigned = 0
        for i, allocation in enumerate(allocations):
            if i < available_faculty.count():
                faculty = available_faculty[i]
                if not InvigilationDuty.objects.filter(faculty=faculty, exam=exam).exists():
                    InvigilationDuty.objects.create(
                        faculty=faculty,
                        exam=exam,
                        room=allocation.room,
                        duty_date=exam.exam_date,
                        reporting_time=exam.start_time,
                        status='assigned'
                    )
                    faculty.duty_count += 1
                    faculty.save()
                    Notification.objects.create(
                        faculty=faculty,
                        title='New Invigilation Duty Assigned',
                        message=f'You have been assigned invigilation for {exam.subject_name} on {exam.exam_date} in Room {allocation.room.room_number}.',
                        notification_type='duty_assigned'
                    )
                    assigned += 1
        messages.success(request, f'{assigned} duties auto-assigned successfully!')
        return redirect('duty_list')
    exams = Exam.objects.filter(status='upcoming')
    return render(request, 'exam_system/auto_assign.html', {'exams': exams})


# ─── NOTIFICATIONS ──────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def notification_list(request):
    notifications = Notification.objects.select_related('faculty').order_by('-created_at')
    return render(request, 'exam_system/notification_list.html', {'notifications': notifications})


@login_required
@user_passes_test(is_admin)
def send_notification(request):
    form = NotificationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        send_all = form.cleaned_data.get('send_to_all')
        if send_all:
            for faculty in Faculty.objects.all():
                Notification.objects.create(
                    faculty=faculty,
                    title=form.cleaned_data['title'],
                    message=form.cleaned_data['message'],
                    notification_type=form.cleaned_data['notification_type']
                )
            messages.success(request, f'Notification sent to all faculty members!')
        else:
            form.save()
            messages.success(request, 'Notification sent!')
        return redirect('notification_list')
    return render(request, 'exam_system/notification_form.html', {'form': form, 'title': 'Send Notification'})


# ─── FACULTY VIEWS ──────────────────────────────────────────────────────────

@login_required
def my_duties(request):
    try:
        faculty = Faculty.objects.get(user=request.user)
        duties = InvigilationDuty.objects.filter(faculty=faculty).select_related('exam', 'room').order_by('duty_date')
        return render(request, 'exam_system/my_duties.html', {'faculty': faculty, 'duties': duties})
    except Faculty.DoesNotExist:
        messages.error(request, 'No faculty profile found.')
        return redirect('dashboard')


@login_required
def my_notifications(request):
    try:
        faculty = Faculty.objects.get(user=request.user)
        notifications = Notification.objects.filter(faculty=faculty).order_by('-created_at')
        notifications.filter(is_read=False).update(is_read=True)
        return render(request, 'exam_system/my_notifications.html', {'faculty': faculty, 'notifications': notifications})
    except Faculty.DoesNotExist:
        return redirect('dashboard')


# ─── REPORTS ────────────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def reports(request):
    faculty_stats = Faculty.objects.annotate(assigned=Count('duties')).order_by('-assigned')
    exam_stats = Exam.objects.annotate(assigned=Count('duties'))
    return render(request, 'exam_system/reports.html', {
        'faculty_stats': faculty_stats,
        'exam_stats': exam_stats,
        'total_duties': InvigilationDuty.objects.count(),
        'completed': InvigilationDuty.objects.filter(status='completed').count(),
        'pending': InvigilationDuty.objects.filter(status='assigned').count(),
    })


@login_required
@user_passes_test(is_admin)
def export_duties_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="invigilation_duties.csv"'
    writer = csv.writer(response)
    writer.writerow(['Faculty', 'Employee ID', 'Department', 'Exam', 'Subject Code', 'Date', 'Reporting Time', 'Room', 'Status'])
    for duty in InvigilationDuty.objects.select_related('faculty', 'exam', 'room', 'faculty__department'):
        writer.writerow([
            duty.faculty.name, duty.faculty.employee_id,
            duty.faculty.department.name if duty.faculty.department else '',
            duty.exam.subject_name, duty.exam.subject_code,
            duty.duty_date, duty.reporting_time, duty.room.room_number, duty.status
        ])
    return response


# ─── DEPARTMENTS ────────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def department_list(request):
    departments = Department.objects.annotate(faculty_count=Count('faculty'))
    return render(request, 'exam_system/department_list.html', {'departments': departments})


@login_required
@user_passes_test(is_admin)
def department_add(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Department added!')
        return redirect('department_list')
    return render(request, 'exam_system/department_form.html', {'form': form, 'title': 'Add Department'})


@login_required
@user_passes_test(is_admin)
def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=dept)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Department updated!')
        return redirect('department_list')
    return render(request, 'exam_system/department_form.html', {'form': form, 'title': 'Edit Department', 'obj': dept})
