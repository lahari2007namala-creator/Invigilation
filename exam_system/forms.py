from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Faculty, Exam, ExamRoom, RoomAllocation, InvigilationDuty, Department, Notification


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['employee_id', 'name', 'email', 'phone', 'department', 'designation', 'is_available']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject_name', 'subject_code', 'department', 'semester', 'exam_date', 'start_time', 'end_time', 'total_students', 'status']
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'form-control'}),
            'subject_code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'total_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class ExamRoomForm(forms.ModelForm):
    class Meta:
        model = ExamRoom
        fields = ['room_number', 'building', 'capacity', 'floor']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'building': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RoomAllocationForm(forms.ModelForm):
    class Meta:
        model = RoomAllocation
        fields = ['exam', 'room', 'students_count']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-select'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
            'students_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class InvigilationDutyForm(forms.ModelForm):
    class Meta:
        model = InvigilationDuty
        fields = ['faculty', 'exam', 'room', 'duty_date', 'reporting_time', 'status', 'notes']
        widgets = {
            'faculty': forms.Select(attrs={'class': 'form-select'}),
            'exam': forms.Select(attrs={'class': 'form-select'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
            'duty_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reporting_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty'].queryset = Faculty.objects.filter(is_available=True)


class NotificationForm(forms.ModelForm):
    send_to_all = forms.BooleanField(required=False, label="Send to All Faculty",
                                      widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Notification
        fields = ['faculty', 'title', 'message', 'notification_type']
        widgets = {
            'faculty': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'notification_type': forms.Select(attrs={'class': 'form-select'}),
        }
