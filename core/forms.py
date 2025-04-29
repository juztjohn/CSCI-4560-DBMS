from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Appointment, Message
from datetime import date, timedelta, datetime

FACILITIES = [
    ('Murfreesboro Clinic', 'Murfreesboro Clinic'),
    ('Smyrna Clinic', 'Smyrna Clinic'),
]

TIMES = [
    ('09:00', '09:00 AM'),
    ('09:30', '09:30 AM'),
    ('10:00', '10:00 AM'),
    ('10:30', '10:30 AM'),
    ('11:00', '11:00 AM'),
    ('11:30', '11:30 AM'),
    ('14:00', '02:00 PM'),
    ('14:30', '02:30 PM'),
    ('15:00', '03:00 PM'),
    ('15:30', '03:30 PM'),
]

class PatientSignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name  = self.cleaned_data.get('last_name')
        user.email      = self.cleaned_data.get('email')
        if commit:
            user.save()
            # Create the Patient profile. Note: if phone is unique, ensure the data is valid.
            Patient.objects.create(user=user, phone=self.cleaned_data.get('phone'))
        return user

class AppointmentForm(forms.ModelForm):
    facility = forms.ChoiceField(choices=FACILITIES)
    appointment_type = forms.CharField(label='Reason for appointment', max_length=50)
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Select a date (up to 3 months out)'
    )
    time = forms.ChoiceField(choices=TIMES, help_text='Select a time slot')
    notes = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Appointment
        # we exclude patient (auto‑set in the view) and date_time (we build it ourselves)
        exclude = ['patient', 'date_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        max_date = today + timedelta(days=90)
        # enforce the 3‑month limit in the widget
        self.fields['date'].widget.attrs['min'] = today.isoformat()
        self.fields['date'].widget.attrs['max'] = max_date.isoformat()

    def save(self, commit=True, patient=None):
        # Build the Appointment instance without writing to DB yet
        appt = super().save(commit=False)
        # combine date + time into the model’s date_time
        dt = f"{self.cleaned_data['date']} {self.cleaned_data['time']}"
        appt.date_time = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        if patient:
            appt.patient = patient
        if commit:
            appt.save()
        return appt

class PatientUpdateForm(forms.ModelForm):
    # These fields are from the User model
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, required=True)

    class Meta:
        model = Patient
        fields = ['phone']  # This is the Patient model field

    def __init__(self, *args, **kwargs):
        # Pop the user instance passed in
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            # Initialize form fields with user data
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            self.fields['username'].initial = self.user.username

    def save(self, commit=True):
        patient = super().save(commit=False)

        # Update User model fields
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            self.user.username = self.cleaned_data['username']
            if commit:
                self.user.save()

        if commit:
            patient.save()

        return patient
    
class PatientMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['doctor', 'message']

class DoctorMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['patient', 'message']
