from django.db import models
from patients.models import Patient
from doctors.models import Doctor
import uuid
from datetime import date

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    )

    appointment_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    reason_for_visit = models.CharField(max_length=255, help_text="Primary complaint or routine visit reason")
    doctor_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date', 'appointment_time']
        # Prevent exact duplicate slots for the same doctor unless cancelled
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date', 'appointment_time'],
                name='unique_doctor_slot'
            )
        ]

    def __str__(self):
        return f"{self.appointment_id}: {self.patient.full_name} with Dr. {self.doctor.full_name} on {self.appointment_date} {self.appointment_time}"

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            today_str = date.today().strftime('%y%m')
            random_part = uuid.uuid4().hex[:4].upper()
            self.appointment_id = f"APT-{today_str}-{random_part}"
        super().save(*args, **kwargs)
