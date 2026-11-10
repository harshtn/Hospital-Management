from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from datetime import date

from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from medical_records.models import MedicalRecord
from billing.models import Invoice
from core.models import Department, Room

def dashboard_view(request):
    today = date.today()

    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    active_doctors = Doctor.objects.filter(is_active=True).count()
    
    total_appointments = Appointment.objects.count()
    today_appointments_count = Appointment.objects.filter(appointment_date=today).count()
    pending_appointments_count = Appointment.objects.filter(status='SCHEDULED').count()
    
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='AVAILABLE').count()
    
    total_revenue = Invoice.objects.filter(payment_status='PAID').aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0.00
    pending_invoices_count = Invoice.objects.filter(payment_status='PENDING').count()

    # Lists for quick viewing on Dashboard
    today_appointments = Appointment.objects.select_related('patient', 'doctor', 'doctor__department')\
        .filter(appointment_date=today).order_by('appointment_time')[:8]
    
    recent_patients = Patient.objects.all().order_by('-created_at')[:6]
    recent_records = MedicalRecord.objects.select_related('patient', 'doctor').order_by('-created_at')[:5]

    # Department distribution data for Chart.js
    dept_labels = []
    dept_doctor_counts = []
    for dept in Department.objects.annotate(doc_count=Count('doctors')).order_by('-doc_count')[:6]:
        dept_labels.append(dept.name)
        dept_doctor_counts.append(dept.doc_count)

    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'active_doctors': active_doctors,
        'total_appointments': total_appointments,
        'today_appointments_count': today_appointments_count,
        'pending_appointments_count': pending_appointments_count,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_revenue': total_revenue,
        'pending_invoices_count': pending_invoices_count,
        'today_appointments': today_appointments,
        'recent_patients': recent_patients,
        'recent_records': recent_records,
        'dept_labels': dept_labels,
        'dept_doctor_counts': dept_doctor_counts,
        'today': today,
    }
    return render(request, 'dashboard.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}. Welcome to HMS 2025!")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration error. Please check requirements.")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

