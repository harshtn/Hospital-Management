from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
import uuid
from datetime import date

class MedicalRecord(models.Model):
    record_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='medical_records')
    record_date = models.DateField(default=date.today)
    
    # Clinical details
    symptoms = models.TextField(help_text="Reported symptoms")
    diagnosis = models.CharField(max_length=255, help_text="Clinical diagnosis")
    treatment_plan = models.TextField(help_text="Detailed treatment recommendations and procedure notes")
    
    # Vital signs
    blood_pressure = models.CharField(max_length=20, blank=True, null=True, help_text="e.g. 120/80 mmHg")
    heart_rate = models.PositiveIntegerField(blank=True, null=True, help_text="bpm")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="°C or °F")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="kg")

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-record_date', '-created_at']

    def __str__(self):
        return f"Record {self.record_id} for {self.patient.full_name} ({self.diagnosis})"

    def save(self, *args, **kwargs):
        if not self.record_id:
            random_part = uuid.uuid4().hex[:4].upper()
            self.record_id = f"REC-{date.today().strftime('%y%m')}-{random_part}"
        super().save(*args, **kwargs)

class PrescriptionItem(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=150)
    dosage = models.CharField(max_length=80, help_text="e.g. 500mg, 1 tablet")
    frequency = models.CharField(max_length=80, help_text="e.g. Twice daily after meals")
    duration_days = models.PositiveIntegerField(default=7, help_text="Duration in days")
    instructions = models.CharField(max_length=255, blank=True, null=True, help_text="Additional precautions")

    def __str__(self):
        return f"{self.medication_name} ({self.dosage}) - {self.frequency}"
