from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    head_of_department = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('GENERAL', 'General Ward'),
        ('PRIVATE', 'Private Room'),
        ('SEMI_PRIVATE', 'Semi-Private Room'),
        ('ICU', 'Intensive Care Unit (ICU)'),
        ('OT', 'Operation Theater'),
        ('EMERGENCY', 'Emergency Ward'),
    )

    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
        ('MAINTENANCE', 'Under Maintenance'),
    )

    room_number = models.CharField(max_length=30, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='GENERAL')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='rooms')
    capacity = models.PositiveIntegerField(default=1)
    current_occupancy = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    cost_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)

    class Meta:
        ordering = ['room_number']

    def __str__(self):
        return f"Room {self.room_number} - {self.get_room_type_display()} ({self.status})"
