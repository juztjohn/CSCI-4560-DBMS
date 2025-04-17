from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import home

urlpatterns = [
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/create_appointment/', views.create_appointment, name='create_appointment'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('', views.home, name='home'),
    path('doctor/patients/doctor_patient_list/', views.doctor_patient_list, name='doctor_patient_list'),
    path('doctor/patient/<int:pk>/', views.patient_details, name='patient_details'),
    path('registration/patient_signup/', views.patient_signup, name='patient_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('billing/patient_billing/', views.patient_billing, name='patient_billing'),
    path('billing/pay_bill/', views.pay_bill, name='pay_bill'),
    path('labs/labs', views.labs, name='labs'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('patient_updateinfo/', views.patient_updateinfo, name='patient_updateinfo'),
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
    path('messages/', views.user_messages, name='messages'),
    path('messages/create_message/', views.create_message, name='create_message'),
    path('pay_bill/<int:bill_id>/', views.pay_bill, name='pay_bill'),
]
