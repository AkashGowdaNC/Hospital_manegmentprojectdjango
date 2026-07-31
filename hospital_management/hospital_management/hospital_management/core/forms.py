from django import forms
from .models import Patient, Doctor, Appointment, VisitHistory
from django.core.exceptions import ValidationError
from django.utils import timezone

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'contact_number', 'address', 
                 'email', 'emergency_contact', 'blood_group', 'allergies', 'medical_history']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'placeholder': 'Enter full name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'min': '0',
                'max': '120'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'placeholder': '+91-9876543210'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'rows': 3,
                'placeholder': 'Enter complete address'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'placeholder': 'patient@example.com'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'placeholder': '+91-9876543210'
            }),
            'blood_group': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'placeholder': 'A+'
            }),
            'allergies': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'rows': 2,
                'placeholder': 'List any allergies'
            }),
            'medical_history': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'rows': 3,
                'placeholder': 'Previous medical conditions, surgeries, etc.'
            }),
        }
    
    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0 or age > 120:
            raise ValidationError("Age must be between 0 and 120 years.")
        return age

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'qualification', 'experience', 
                 'contact_number', 'email', 'consultation_fee', 'available_from', 
                 'available_to', 'is_available', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'placeholder': 'Dr. Full Name'
            }),
            'specialization': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent'
            }),
            'qualification': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'placeholder': 'MBBS, MD, etc.'
            }),
            'experience': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'min': '0'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'placeholder': '+91-9876543210'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'placeholder': 'doctor@cloverhospital.com'
            }),
            'consultation_fee': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'step': '0.01',
                'min': '0'
            }),
            'available_from': forms.TimeInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'type': 'time'
            }),
            'available_to': forms.TimeInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'type': 'time'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-hospital-mint border-gray-300 rounded focus:ring-hospital-mint'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'rows': 3,
                'placeholder': 'Doctor\'s biography and expertise...'
            }),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time_slot', 'appointment_type', 'reason']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent'
            }),
            'doctor': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'id': 'doctor-select'
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'type': 'date',
                'id': 'appointment-date'
            }),
            'time_slot': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'id': 'time-slot-select'
            }),
            'appointment_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'rows': 3,
                'placeholder': 'Reason for appointment...'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')
        
        if doctor and date and time_slot:
            # Check if appointment already exists (exclude current instance if updating)
            queryset = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time_slot=time_slot,
                status__in=['SCHEDULED', 'COMPLETED']
            )
            # Exclude current instance if this is an update
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise ValidationError(
                    f"Dr. {doctor.name} is already booked for {date} at {time_slot}. Please choose a different time slot."
                )
        
        # Check if date is in the past
        if date and date < timezone.now().date():
            raise ValidationError("Cannot book appointment for past dates.")
        
        return cleaned_data

class VisitHistoryForm(forms.ModelForm):
    class Meta:
        model = VisitHistory
        fields = ['diagnosis', 'symptoms', 'prescription', 'tests_recommended', 'follow_up_date', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'rows': 3,
                'placeholder': 'Enter diagnosis...'
            }),
            'symptoms': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'rows': 3,
                'placeholder': 'Describe symptoms...'
            }),
            'prescription': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'rows': 4,
                'placeholder': 'Enter prescription details...'
            }),
            'tests_recommended': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'rows': 2,
                'placeholder': 'Recommended tests...'
            }),
            'follow_up_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-hospital-mint focus:border-transparent',
                'rows': 2,
                'placeholder': 'Additional notes...'
            }),
        }