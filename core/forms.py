from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Appointment, Message

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
    class Meta:
        model = Appointment
        fields = ['facility', 'doctor', 'appointment_type', 'date_time', 'notes']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:shadow-outline'}),
        }

class PatientMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['doctor', 'message']

class DoctorMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['patient', 'message']