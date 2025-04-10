from django.urls import path
from . import views
from .views import patient_dashboard, home

urlpatterns = [
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('register/', views.patient_registration, name='patient_registration'),
    path('', views.home, name='home'),
    path('signup/', views.patient_signup, name='patient_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient_billing/', views.patient_billing, name='patient_billing'),
    path('pay_bill/', views.pay_bill, name='pay_bill'),
]
