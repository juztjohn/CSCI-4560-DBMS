from django.db import models
from django.contrib.auth.models import User  # using built-in User model for accounts
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import date, datetime

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

class Lab(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test = models.CharField(max_length=100, default='Flu')
    test_result = models.CharField(max_length=100, default='Negative')
    date = models.DateField(default=date.today)

    class Meta:
        ordering = ['date']

class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid')],
        default='Pending'
    )
    insurance = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Billing for {self.patient} - {self.amount_due}"

class Message(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.CharField(unique_for_date='date')
    date = models.DateField(default=date.today)
    time = models.TimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['date', 'time']
