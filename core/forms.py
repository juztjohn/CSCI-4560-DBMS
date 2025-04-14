from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Appointment

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