from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Faculty
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/add/', views.faculty_add, name='faculty_add'),
    path('faculty/<int:pk>/edit/', views.faculty_edit, name='faculty_edit'),
    path('faculty/<int:pk>/delete/', views.faculty_delete, name='faculty_delete'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),

    # Exams
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/add/', views.exam_add, name='exam_add'),
    path('exams/<int:pk>/edit/', views.exam_edit, name='exam_edit'),
    path('exams/<int:pk>/delete/', views.exam_delete, name='exam_delete'),

    # Rooms
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),

    # Room Allocations
    path('allocations/', views.allocation_list, name='allocation_list'),
    path('allocations/add/', views.allocation_add, name='allocation_add'),
    path('allocations/<int:pk>/delete/', views.allocation_delete, name='allocation_delete'),

    # Duties
    path('duties/', views.duty_list, name='duty_list'),
    path('duties/add/', views.duty_add, name='duty_add'),
    path('duties/<int:pk>/edit/', views.duty_edit, name='duty_edit'),
    path('duties/<int:pk>/delete/', views.duty_delete, name='duty_delete'),
    path('duties/auto-assign/', views.auto_assign_duties, name='auto_assign_duties'),

    # Notifications
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/send/', views.send_notification, name='send_notification'),

    # Faculty views
    path('my-duties/', views.my_duties, name='my_duties'),
    path('my-notifications/', views.my_notifications, name='my_notifications'),

    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/export/', views.export_duties_csv, name='export_duties_csv'),

    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_add, name='department_add'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),
]
