from django import forms
from django.forms import inlineformset_factory
from .models import MedicalRecord, PrescriptionItem

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            'patient', 'doctor', 'appointment', 'record_date',
            'symptoms', 'diagnosis', 'treatment_plan',
            'blood_pressure', 'heart_rate', 'temperature', 'weight_kg', 'notes'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'appointment': forms.Select(attrs={'class': 'form-select'}),
            'record_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Symptoms described by patient'}),
            'diagnosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Confirmed or suspected diagnosis'}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Plan of care, advice, referral notes'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 120/80'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'bpm'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '°C'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'kg'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Internal staff notes'}),
        }

class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ['medication_name', 'dosage', 'frequency', 'duration_days', 'instructions']
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medication name'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dosage (e.g. 500mg)'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Frequency (e.g. 2x daily)'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'instructions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instructions / Notes'}),
        }

PrescriptionFormSet = inlineformset_factory(
    MedicalRecord,
    PrescriptionItem,
    form=PrescriptionItemForm,
    extra=2,
    can_delete=True
)

