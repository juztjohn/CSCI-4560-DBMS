# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Patient, Appointment
from .forms import PatientSignUpForm

def home(request):
    return render(request, 'home.html')

@login_required  # ensures only authenticated users access this view
def appointment_list(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('patient_registration')  # Replace with the appropriate URL
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'appointments_list.html', {'appointments': appointments})

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

    appointments = Appointment.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'patient_dashboard.html', context)

@login_required
def dashboard(request):
    user = request.user
    context = {}

    # Check if the user is a superuser (admin)
    if user.is_superuser:
        context['role'] = 'admin'
        # Optionally, add admin-specific context data
    elif hasattr(user, 'doctor'):
        context['role'] = 'doctor'
        # Fetch doctor-specific data, e.g.:
        # context['appointments'] = Appointment.objects.filter(doctor=user.doctor)
    elif hasattr(user, 'receptionist'):
        context['role'] = 'receptionist'
        # Fetch receptionist-specific data here
    elif hasattr(user, 'patient'):
        context['role'] = 'patient'
        patient = user.patient
        context['patient'] = patient
        context['appointments'] = Appointment.objects.filter(patient=patient)
    else:
        context['role'] = 'unknown'

    return render(request, 'dashboard.html', context)

@login_required  # ensures only authenticated users access this view
def patient_billing(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('patient_registration')  # Replace with the appropriate URL
    return render(request, 'patient_billing.html')

@login_required  # ensures only authenticated users access this view
def pay_bill(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('patient_registration')  # Replace with the appropriate URL
    return render(request, 'pay_bill.html')
