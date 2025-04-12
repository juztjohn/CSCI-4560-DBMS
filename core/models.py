from django.db import models
from django.contrib.auth.models import User  # using built-in User model for accounts
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # link to auth user
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)        # each patient has unique phone
    # add other patient-specific fields, e.g., address, medical_record_number, etc.

    def __str__(self):
        return f"{self.user.get_full_name()}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    # e.g., a doctor might have a license_id that's unique:
    license_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Dr. {self.user.last_name} ({self.specialty})"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    facility = models.CharField(max_length=100, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_type = models.CharField(max_length=50, default='Checkup')
    facility = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_type = models.CharField(max_length=50)
    date_time = models.DateTimeField(default=timezone.now)  # now as default
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = [('patient', 'doctor', 'date_time')]
        ordering = ['date_time']

    def __str__(self):
        return f"Appointment on {self.date_time:%Y-%m-%d %H:%M} with {self.doctor}"
