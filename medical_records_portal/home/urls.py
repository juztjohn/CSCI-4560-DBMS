from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('patient/', views.patient, name='patient'),
    path('appointments/', views.appointments_view, name = 'appointments'),
]