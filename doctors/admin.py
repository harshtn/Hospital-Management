from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'full_name', 'department', 'specialization', 'phone', 'consultation_fee', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('doctor_id', 'first_name', 'last_name', 'specialization', 'email')
    readonly_fields = ('doctor_id', 'created_at')

