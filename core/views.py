from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .models import Patient, Doctor, Appointment, Lab, Billing, Message
from .forms import PatientSignUpForm, AppointmentForm, PatientUpdateForm, PatientMessageForm, DoctorMessageForm

def home(request):
    return render(request, 'home.html')

@login_required
def appointments(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return redirect('registration/patient_signup')
    appts = Appointment.objects.filter(patient=patient)
    return render(request, 'appointments/appointments.html', {'appointments': appts})

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PatientSignUpForm()
    return render(request, 'registration/patient_signup.html', {'form': form})

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
def doctor_patient_list(request):
    doctor = request.user.doctor
    # get distinct patients with latest appointment date
    patients = (
        Patient.objects
        .filter(appointment__doctor=doctor)
        .annotate(last_appointment=Max('appointment__date_time'))
        .order_by('-last_appointment')
    )
    return render(request, 'doctor/patients/doctor_patient_list.html', {'patients': patients})

@login_required
def patient_details(request, pk):
    # only doctors should hit this; you can check request.user.doctor here if needed
    patient = get_object_or_404(Patient, pk=pk)
    # example related data
    appointments = Appointment.objects.filter(patient=patient).order_by('-date_time')
    labs         = Lab.objects.filter(patient=patient).order_by('-date')
    bills        = Billing.objects.filter(patient=patient).order_by('-created_at')
    return render(request, 'doctor/patient_details.html', {
        'patient': patient,
        'appointments': appointments,
        'labs': labs,
        'bills': bills,
    })

@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # pass the patient in so form.save() can set it
            form.save(patient=request.user.patient)
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
        return redirect('registration/patient_signup')
    bills = Billing.objects.filter(patient=patient)
    return render(request, 'billing/patient_billing.html', {'bills': bills})

@login_required 
def pay_bill(request, bill_id):
    bill = get_object_or_404(Billing,
                             id=bill_id,
                             patient=request.user.patient)
    if request.method == 'POST':
        bill.delete()  
        messages.success(request, "Bill paid and removed.")
        return redirect('patient_billing')

@login_required
def labs(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You do not have a patient profile. Please complete your registration.")
        return redirect('registration/patient_signup')

    patient_labs = Lab.objects.filter(patient=patient)
    return render(request, 'labs/labs.html', {'labs': patient_labs})

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

    if hasattr(user, 'patient'):
        patient_messages = Message.objects.filter(patient=user.patient)
        return render(request, 'messages/messages.html', {'messages': patient_messages})
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
