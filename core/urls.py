from django.urls import path
from . import views
from .views import patient_dashboard, home

urlpatterns = [
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/create_appointment/', views.create_appointment, name='create_appointment'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('register/', views.patient_registration, name='patient_registration'),
    path('', views.home, name='home'),
    path('signup/', views.patient_signup, name='patient_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
