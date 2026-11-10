from django.db import models
from core.models import Department
import uuid

class Doctor(models.Model):
    doctor_id = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')
    specialization = models.CharField(max_length=120)
    qualification = models.CharField(max_length=150, help_text="e.g. MBBS, MD, FRCS")
    experience_years = models.PositiveIntegerField(default=1)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    room_number = models.CharField(max_length=30, blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    
    # Availability
    available_days = models.CharField(
        max_length=150, 
        default="Monday, Tuesday, Wednesday, Thursday, Friday",
        help_text="Comma-separated working days"
    )
    time_slot_start = models.TimeField(default='09:00:00')
    time_slot_end = models.TimeField(default='17:00:00')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"Dr. {self.full_name} ({self.specialization})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.doctor_id:
            random_part = uuid.uuid4().hex[:4].upper()
            self.doctor_id = f"DOC-{random_part}"
        super().save(*args, **kwargs)

