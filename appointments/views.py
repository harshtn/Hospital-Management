from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from .models import Appointment
from .forms import AppointmentForm
from doctors.models import Doctor

def appointment_list(request):
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()
    doctor_id = request.GET.get('doctor', '').strip()
    date_filter = request.GET.get('date', '').strip()

    appointments = Appointment.objects.select_related('patient', 'doctor', 'doctor__department').all()

    if search_query:
        appointments = appointments.filter(
            Q(appointment_id__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(doctor__first_name__icontains=search_query) |
            Q(doctor__last_name__icontains=search_query) |
            Q(reason_for_visit__icontains=search_query)
        )

    if status_filter:
        appointments = appointments.filter(status=status_filter)

    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)

    if date_filter == 'today':
        appointments = appointments.filter(appointment_date=date.today())
    elif date_filter == 'upcoming':
        appointments = appointments.filter(appointment_date__gte=date.today())
    elif date_filter == 'past':
        appointments = appointments.filter(appointment_date__lt=date.today())
    elif date_filter:
        appointments = appointments.filter(appointment_date=date_filter)

    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    doctors = Doctor.objects.filter(is_active=True)
    statuses = Appointment.STATUS_CHOICES

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'selected_doctor': doctor_id,
        'date_filter': date_filter,
        'doctors': doctors,
        'statuses': statuses,
        'total_count': appointments.count()
    }
    return render(request, 'appointments/appointment_list.html', context)

def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment.objects.select_related('patient', 'doctor', 'doctor__department'), pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})

def appointment_create(request):
    initial = {}
    if 'patient_id' in request.GET:
        initial['patient'] = request.GET.get('patient_id')
    if 'doctor_id' in request.GET:
        initial['doctor'] = request.GET.get('doctor_id')
    if 'date' in request.GET:
        initial['appointment_date'] = request.GET.get('date')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f"Appointment {appointment.appointment_id} scheduled successfully.")
            return redirect('appointment_detail', pk=appointment.pk)
        else:
            messages.error(request, "Failed to schedule appointment. Please check the inputs.")
    else:
        form = AppointmentForm(initial=initial)

    return render(request, 'appointments/appointment_form.html', {'form': form, 'title': 'Schedule New Appointment'})

def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f"Appointment {appointment.appointment_id} updated successfully.")
            return redirect('appointment_detail', pk=appointment.pk)
        else:
            messages.error(request, "Please check the form inputs.")
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/appointment_form.html', {
        'form': form,
        'title': f"Reschedule / Edit Appointment #{appointment.appointment_id}",
        'appointment': appointment
    })

def appointment_status_update(request, pk, new_status):
    appointment = get_object_or_404(Appointment, pk=pk)
    valid_statuses = dict(Appointment.STATUS_CHOICES)
    if new_status in valid_statuses:
        appointment.status = new_status
        appointment.save()
        messages.success(request, f"Appointment status changed to {valid_statuses[new_status]}.")
    else:
        messages.error(request, "Invalid status choice.")
    return redirect('appointment_detail', pk=pk)
