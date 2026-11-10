from django.contrib import admin
from .models import MedicalRecord, PrescriptionItem

class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'patient', 'doctor', 'diagnosis', 'record_date', 'created_at')
    list_filter = ('record_date', 'doctor')
    search_fields = ('record_id', 'patient__first_name', 'patient__last_name', 'diagnosis', 'symptoms')
    readonly_fields = ('record_id', 'created_at')
    inlines = [PrescriptionItemInline]

