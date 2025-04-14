from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import home

urlpatterns = [
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/create_appointment/', views.create_appointment, name='create_appointment'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('', views.home, name='home'),
    path('signup/', views.patient_signup, name='patient_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient_billing/', views.patient_billing, name='patient_billing'),
    path('pay_bill/', views.pay_bill, name='pay_bill'),
    path('labs/', views.labs, name='labs'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
