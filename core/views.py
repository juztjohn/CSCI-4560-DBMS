# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Patient, Appointment
from .forms import PatientSignUpForm, AppointmentForm

def home(request):
    return render(request, 'home.html')

<<<<<<< HEAD
@login_required  # ensures only authenticated users access this view
=======
@login_required
>>>>>>> main
def appointments(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
<<<<<<< HEAD
        return redirect('patient_registration')  # Replace with the appropriate URL
=======
        return redirect('patient_registration')
>>>>>>> main
    # Retrieve appointments for the patient
    appts = Appointment.objects.filter(patient=patient)
    return render(request, 'appointments/appointments.html', {'appointments': appts})

def patient_registration(request):
    return render(request, 'patient_registration.html')

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PatientSignUpForm()
    return render(request, 'patient_signup.html', {'form': form})

@login_required
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return redirect('patient_registration')
    appts = Appointment.objects.filter(patient=patient)
    context = {
        'patient': patient,
        'appointments': appts,
    }
    return render(request, 'patient_dashboard.html', context)

@login_required
def dashboard(request):
    user = request.user
    context = {}
    if user.is_superuser:
        context['role'] = 'admin'
    elif hasattr(user, 'doctor'):
        context['doctor_appointments'] = Appointment.objects.filter(doctor=user.doctor)
        context['role'] = 'doctor'
    elif hasattr(user, 'receptionist'):
        context['role'] = 'receptionist'
    elif hasattr(user, 'patient'):
        context['role'] = 'patient'
        patient = user.patient
        context['patient'] = patient
        context['appointments'] = Appointment.objects.filter(patient=patient)
    else:
        context['role'] = 'unknown'
    return render(request, 'dashboard.html', context)

@login_required
def doctor_appointments(request):
    try:
        doctor = request.user.doctor
        appts = Appointment.objects.filter(doctor=doctor)
    except AttributeError:
        appts = Appointment.objects.none()
    return render(request, 'doctor/doctor_appointments.html', {'appointments': appts})

@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('appointments')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/create_appointment.html', {'form': form})

<<<<<<< HEAD
@login_required 
def patient_billing(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('patient_registration')
    return render(request, 'patient_billing.html')

@login_required 
def pay_bill(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('patient_registration') 
    return render(request, 'pay_bill.html')
=======
>>>>>>> main
