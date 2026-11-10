from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'full_name', 'gender', 'age', 'blood_group', 'phone', 'status', 'created_at')
    list_filter = ('gender', 'blood_group', 'status')
    search_fields = ('patient_id', 'first_name', 'last_name', 'phone', 'email')
    readonly_fields = ('patient_id', 'created_at', 'updated_at')

