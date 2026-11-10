from rest_framework import serializers
from core.models import Department, Room
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from medical_records.models import MedicalRecord, PrescriptionItem
from billing.models import Invoice, InvoiceItem

class DepartmentSerializer(serializers.ModelSerializer):
    doctor_count = serializers.IntegerField(source='doctors.count', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'head_of_department', 'phone', 'doctor_count', 'created_at']

class RoomSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_number', 'room_type', 'department', 'department_name', 'capacity', 'current_occupancy', 'status', 'cost_per_day']

class DoctorSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'doctor_id', 'first_name', 'last_name', 'full_name',
            'department', 'department_name', 'specialization', 'qualification',
            'experience_years', 'phone', 'email', 'room_number', 'consultation_fee',
            'available_days', 'time_slot_start', 'time_slot_end', 'is_active', 'created_at'
        ]

class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'patient_id', 'first_name', 'last_name', 'full_name', 'age',
            'gender', 'date_of_birth', 'blood_group', 'phone', 'email', 'address',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'allergies', 'chronic_conditions', 'medical_history',
            'insurance_provider', 'insurance_policy_number', 'status',
            'created_at', 'updated_at'
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    department_name = serializers.CharField(source='doctor.department.name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'appointment_id', 'patient', 'patient_name',
            'doctor', 'doctor_name', 'department_name',
            'appointment_date', 'appointment_time', 'status',
            'reason_for_visit', 'doctor_notes', 'created_at', 'updated_at'
        ]

class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medication_name', 'dosage', 'frequency', 'duration_days', 'instructions']

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    prescriptions = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'record_id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'appointment', 'record_date', 'symptoms', 'diagnosis', 'treatment_plan',
            'blood_pressure', 'heart_rate', 'temperature', 'weight_kg', 'notes',
            'prescriptions', 'created_at'
        ]

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'unit_price', 'quantity', 'total']

class InvoiceSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_id = serializers.CharField(source='patient.patient_id', read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)
    balance_due = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_id', 'patient', 'patient_id', 'patient_name',
            'appointment', 'issue_date', 'due_date', 'subtotal', 'discount',
            'tax', 'total_amount', 'paid_amount', 'balance_due',
            'payment_status', 'payment_method', 'notes', 'items', 'created_at'
        ]

