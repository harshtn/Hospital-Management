from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Patient
from .forms import PatientForm

def patient_list(request):
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()
    blood_group_filter = request.GET.get('blood_group', '').strip()

    patients = Patient.objects.all()

    if search_query:
        patients = patients.filter(
            Q(patient_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    if status_filter:
        patients = patients.filter(status=status_filter)

    if blood_group_filter:
        patients = patients.filter(blood_group=blood_group_filter)

    paginator = Paginator(patients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    blood_groups = Patient.BLOOD_GROUP_CHOICES
    statuses = Patient.STATUS_CHOICES

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'blood_group_filter': blood_group_filter,
        'blood_groups': blood_groups,
        'statuses': statuses,
        'total_count': patients.count()
    }
    return render(request, 'patients/patient_list.html', context)

def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    # Related appointments, medical records, and invoices
    appointments = patient.appointments.all().order_by('-appointment_date', '-appointment_time')[:5]
    records = patient.medical_records.all().order_by('-record_date')[:5]
    invoices = patient.invoices.all().order_by('-issue_date')[:5]

    context = {
        'patient': patient,
        'appointments': appointments,
        'records': records,
        'invoices': invoices,
    }
    return render(request, 'patients/patient_detail.html', context)

def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f"Patient {patient.full_name} ({patient.patient_id}) created successfully.")
            return redirect('patient_detail', pk=patient.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PatientForm()

    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Register New Patient'})

def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f"Patient records for {patient.full_name} updated successfully.")
            return redirect('patient_detail', pk=patient.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/patient_form.html', {'form': form, 'title': f"Edit {patient.full_name}", 'patient': patient})

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        name = patient.full_name
        patient.delete()
        messages.success(request, f"Patient {name} deleted successfully.")
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})

