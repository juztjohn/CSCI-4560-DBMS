# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, Appointment, Lab, Billing, Message
from .forms import PatientSignUpForm, AppointmentForm, PatientUpdateForm, PatientMessageForm, DoctorMessageForm

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
    if request.method == 'POST':
        bill_id = request.POST.get('selected_bill')
    
        if bill_id:
            try:
                bill = get_object_or_404(Billing, id=bill_id)
                return render(request, 'pay_bill.html', {"bill": bill})
            except (ValueError, TypeError):
                pass # ignore button

    # If no bill was selected or method isn't POST
    return render(request, 'patient_billing.html')

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
def patient_updateinfo(request):
    patient = Patient.objects.get(user=request.user)
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, instance=patient, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('dashboard')  # or wherever you want to redirect
    else:
        form = PatientUpdateForm(instance=patient, user=request.user)

    return render(request, 'patient_updateinfo.html', {'form': form})


@login_required
def confirm_payment(request):
    if request.method == 'POST':
        bill_id = request.POST.get('bill_id')
        if bill_id:
            bill = get_object_or_404(Billing, id=bill_id)
            bill.payment_status = 'Paid'
            bill.save()
            return redirect('patient_billing')
    return redirect('patient_billing')

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
