from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import MedicalRecord
from .forms import MedicalRecordForm, PrescriptionFormSet

def record_list(request):
    search_query = request.GET.get('search', '').strip()
    records = MedicalRecord.objects.select_related('patient', 'doctor').all()

    if search_query:
        records = records.filter(
            Q(record_id__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(diagnosis__icontains=search_query) |
            Q(doctor__first_name__icontains=search_query) |
            Q(doctor__last_name__icontains=search_query)
        )

    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'medical_records/record_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': records.count()
    })

def record_detail(request, pk):
    record = get_object_or_404(
        MedicalRecord.objects.select_related('patient', 'doctor', 'doctor__department').prefetch_related('prescriptions'),
        pk=pk
    )
    return render(request, 'medical_records/record_detail.html', {'record': record})

def record_create(request):
    initial = {}
    if 'patient_id' in request.GET:
        initial['patient'] = request.GET.get('patient_id')
    if 'doctor_id' in request.GET:
        initial['doctor'] = request.GET.get('doctor_id')
    if 'appointment_id' in request.GET:
        initial['appointment'] = request.GET.get('appointment_id')

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        formset = PrescriptionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            record = form.save()
            formset.instance = record
            formset.save()
            messages.success(request, f"Medical record {record.record_id} saved successfully.")
            return redirect('record_detail', pk=record.pk)
        else:
            messages.error(request, "Failed to create medical record. Please inspect errors.")
    else:
        form = MedicalRecordForm(initial=initial)
        formset = PrescriptionFormSet()

    return render(request, 'medical_records/record_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Add Medical Examination Record'
    })

def record_update(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record)
        formset = PrescriptionFormSet(request.POST, instance=record)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f"Medical record {record.record_id} updated successfully.")
            return redirect('record_detail', pk=record.pk)
        else:
            messages.error(request, "Please check the form inputs.")
    else:
        form = MedicalRecordForm(instance=record)
        formset = PrescriptionFormSet(instance=record)

    return render(request, 'medical_records/record_form.html', {
        'form': form,
        'formset': formset,
        'title': f"Edit Medical Record #{record.record_id}",
        'record': record
    })

