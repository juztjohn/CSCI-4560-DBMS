from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta

from django.contrib.auth.models import User
from core.models import Doctor, Patient, Appointment, Lab, Billing

class Command(BaseCommand):
    help = "Seed the database with demo data"

    def handle(self, *args, **options):
        fake = Faker()
        self.stdout.write("Clearing old data…")
        # Optionally wipe old rows
        Appointment.objects.all().delete()
        Lab.objects.all().delete()
        Billing.objects.all().delete()
        Patient.objects.all().delete()
        Doctor.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating doctors…")
        doctors = []
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password="password123"
            )
            doc = Doctor.objects.create(
                user=user,
                specialty=random.choice(['Cardiology','Dermatology','Pediatrics','Oncology','General']),
                license_id=fake.unique.bothify(text='??-#####')
            )
            doctors.append(doc)

        self.stdout.write("Creating patients…")
        patients = []
        for _ in range(20):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password="password123"
            )
            pat = Patient.objects.create(
                user=user,
                phone=fake.phone_number()
            )
            patients.append(pat)

        self.stdout.write("Creating appointments, labs, and billing…")
        for pat in patients:
            # each patient gets 1-3 past appointments
            for _ in range(random.randint(1,3)):
                doc = random.choice(doctors)
                dt = timezone.now() - timedelta(days=random.randint(1,60))
                Appointment.objects.create(
                    patient=pat,
                    doctor=doc,
                    facility=random.choice(['Main Campus','Downtown Clinic']),
                    appointment_type=random.choice(['Checkup','Consultation','Follow‑up','Lab Review']),
                    date_time=dt,
                    notes=fake.sentence(nb_words=6)
                )
            # labs
            for _ in range(random.randint(0,2)):
                Lab.objects.create(
                    patient=pat,
                    test=random.choice(['CBC','Lipid Panel','X‑Ray','MRI']),
                    test_result=random.choice(['Normal','Abnormal','Needs follow‑up']),
                    date=timezone.now().date() - timedelta(days=random.randint(1,60))
                )
            # billing
            for _ in range(random.randint(0,2)):
                Billing.objects.create(
                    patient=pat,
                    amount_due=round(random.uniform(50,500), 2),
                    payment_status=random.choice(['Pending','Paid']),
                    insurance=random.choice(['BlueCross','Aetna','United'])
                )

        self.stdout.write(self.style.SUCCESS("✅ Demo data created successfully!"))

