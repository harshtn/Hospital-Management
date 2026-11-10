from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.db.models import Count, Sum
from datetime import date

from core.models import Department, Room
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from medical_records.models import MedicalRecord
from billing.models import Invoice

from .serializers import (
    DepartmentSerializer, RoomSerializer, DoctorSerializer,
    PatientSerializer, AppointmentSerializer, MedicalRecordSerializer,
    InvoiceSerializer
)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name', 'code', 'head_of_department']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('department').all()
    serializer_class = RoomSerializer
    search_fields = ['room_number', 'room_type']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('department').all()
    serializer_class = DoctorSerializer
    search_fields = ['first_name', 'last_name', 'specialization', 'doctor_id']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_doctors = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(available_doctors, many=True)
        return Response(serializer.data)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    search_fields = ['patient_id', 'first_name', 'last_name', 'phone', 'email']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient', 'doctor', 'doctor__department').all()
    serializer_class = AppointmentSerializer
    search_fields = ['appointment_id', 'patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'reason_for_visit']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    @action(detail=False, methods=['get'])
    def today(self, request):
        today_appointments = self.queryset.filter(appointment_date=date.today())
        serializer = self.get_serializer(today_appointments, many=True)
        return Response(serializer.data)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.select_related('patient', 'doctor').prefetch_related('prescriptions').all()
    serializer_class = MedicalRecordSerializer
    search_fields = ['record_id', 'diagnosis', 'symptoms', 'patient__first_name', 'patient__last_name']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('patient', 'appointment').prefetch_related('items').all()
    serializer_class = InvoiceSerializer
    search_fields = ['invoice_id', 'patient__first_name', 'patient__last_name', 'patient__patient_id']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

class AnalyticsSummaryView(APIView):
    """
    Returns aggregated KPIs and statistics for Dashboard charts and external integrations.
    """
    def get(self, request):
        today = date.today()
        
        total_patients = Patient.objects.count()
        total_doctors = Doctor.objects.count()
        active_doctors = Doctor.objects.filter(is_active=True).count()
        
        total_appointments = Appointment.objects.count()
        today_appointments = Appointment.objects.filter(appointment_date=today).count()
        pending_appointments = Appointment.objects.filter(status='SCHEDULED').count()
        completed_appointments = Appointment.objects.filter(status='COMPLETED').count()

        # Invoices stats
        total_revenue = Invoice.objects.filter(payment_status='PAID').aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0.00
        pending_invoices = Invoice.objects.filter(payment_status='PENDING').count()

        # Department distribution
        dept_distribution = list(
            Doctor.objects.values('department__name')
            .annotate(doctor_count=Count('id'))
            .order_by('-doctor_count')
        )

        # Appointments by status
        status_distribution = list(
            Appointment.objects.values('status')
            .annotate(count=Count('id'))
        )

        return Response({
            'kpis': {
                'total_patients': total_patients,
                'total_doctors': total_doctors,
                'active_doctors': active_doctors,
                'total_appointments': total_appointments,
                'today_appointments': today_appointments,
                'pending_appointments': pending_appointments,
                'completed_appointments': completed_appointments,
                'total_revenue': float(total_revenue),
                'pending_invoices': pending_invoices,
            },
            'dept_distribution': dept_distribution,
            'status_distribution': status_distribution,
        })

