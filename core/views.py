# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, Appointment, Lab, Billing, Message
from .forms import PatientSignUpForm, AppointmentForm, PatientMessageForm, DoctorMessageForm

def home(request):
    return render(request, 'home.html')

@login_required
def appointments(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('patient_signup')
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

@login_required 
def patient_billing(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('patient_registration')
    bills = Billing.objects.filter(patient=patient)
    return render(request, 'patient_billing.html', {'bills': bills})

@login_required 
def pay_bill(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('patient_registration') 
    return render(request, 'pay_bill.html')

@login_required
def labs(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('patient_registration')

    # Retrieve labs for the patient
    patient_labs = Lab.objects.filter(patient=patient)
    return render(request, 'labs.html', {'labs': patient_labs})

@login_required
def user_messages(request):
    try:
        user = request.user
    except User.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('patient_registration')

    # Retrieve messages for the patient
    if hasattr(user, 'patient'):
        patient_messages = Message.objects.filter(patient=user.patient)
        return render(request, 'messages/messages.html', {'messages': patient_messages})
    # Retrieve messages for the doctor
    elif hasattr(user, 'doctor'):
        doctor_messages = Message.objects.filter(doctor=user.doctor)
        return render(request, 'messages/messages.html', {'messages': doctor_messages})
    
@login_required
def create_message(request):
    user = request.user
    if request.method == 'POST':
        if hasattr(user, 'patient'):
            form = PatientMessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.patient = user.patient
                message.created_by = user
                message.save()
                return redirect('messages')
        elif hasattr(user, 'doctor'):
            form = DoctorMessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.doctor = user.doctor
                message.created_by = user
                message.save()
                return redirect('messages')
    else:
        if hasattr(user, 'patient'):
            form = PatientMessageForm()
        elif hasattr(user, 'doctor'):
            form = DoctorMessageForm()
    return render(request, 'messages/create_message.html', {'form': form})