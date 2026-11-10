from django import forms
from .models import Appointment
from datetime import date

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'reason_for_visit', 'status', 'doctor_notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason_for_visit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Chronic chest pain, Annual checkup'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'doctor_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Clinical observations and notes...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        apt_date = cleaned_data.get('appointment_date')
        apt_time = cleaned_data.get('appointment_time')
        status = cleaned_data.get('status')

        if doctor and apt_date and apt_time and status != 'CANCELLED':
            # Check slot conflict
            qs = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=apt_date,
                appointment_time=apt_time
            ).exclude(status='CANCELLED')

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    f"Dr. {doctor.full_name} is already booked on {apt_date} at {apt_time}. Please pick another time slot."
                )

        return cleaned_data

