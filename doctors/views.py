from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Doctor
from .forms import DoctorForm
from core.models import Department

def doctor_list(request):
    search_query = request.GET.get('search', '').strip()
    department_id = request.GET.get('department', '').strip()

    doctors = Doctor.objects.select_related('department').all()

    if search_query:
        doctors = doctors.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(specialization__icontains=search_query) |
            Q(doctor_id__icontains=search_query)
        )

    if department_id:
        doctors = doctors.filter(department_id=department_id)

    paginator = Paginator(doctors, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    departments = Department.objects.all()

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_department': department_id,
        'departments': departments,
        'total_count': doctors.count(),
    }
    return render(request, 'doctors/doctor_list.html', context)

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor.objects.select_related('department'), pk=pk)
    appointments = doctor.appointments.select_related('patient').order_by('-appointment_date', '-appointment_time')[:10]
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
    }
    return render(request, 'doctors/doctor_detail.html', context)

def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f"Dr. {doctor.full_name} registered successfully.")
            return redirect('doctor_detail', pk=doctor.pk)
        else:
            messages.error(request, "Please check the form inputs.")
    else:
        form = DoctorForm()
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Add New Doctor'})

def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f"Dr. {doctor.full_name}'s profile updated successfully.")
            return redirect('doctor_detail', pk=doctor.pk)
        else:
            messages.error(request, "Please check the form inputs.")
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': f"Edit Dr. {doctor.full_name}", 'doctor': doctor})

def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        name = doctor.full_name
        doctor.delete()
        messages.success(request, f"Doctor Dr. {name} removed successfully.")
        return redirect('doctor_list')
    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})
