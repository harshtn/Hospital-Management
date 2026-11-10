from django.db import models
from datetime import date
import uuid

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('UNKNOWN', 'Unknown'),
    )

    STATUS_CHOICES = (
        ('ACTIVE', 'Active / Outpatient'),
        ('INPATIENT', 'Admitted (Inpatient)'),
        ('DISCHARGED', 'Discharged'),
        ('INACTIVE', 'Inactive'),
    )

    patient_id = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, default='UNKNOWN')
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=120)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relation = models.CharField(max_length=50, blank=True, default='Guardian')

    # Medical Background
    allergies = models.TextField(blank=True, null=True, help_text="e.g. Penicillin, Peanuts, Latex")
    chronic_conditions = models.TextField(blank=True, null=True, help_text="e.g. Hypertension, Type 2 Diabetes")
    medical_history = models.TextField(blank=True, null=True)
    
    # Insurance
    insurance_provider = models.CharField(max_length=120, blank=True, null=True)
    insurance_policy_number = models.CharField(max_length=60, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient_id} - {self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Generate PAT-YYYYMM-XXXX
            today_str = date.today().strftime('%y%m')
            random_part = uuid.uuid4().hex[:4].upper()
            self.patient_id = f"PAT-{today_str}-{random_part}"
        super().save(*args, **kwargs)

