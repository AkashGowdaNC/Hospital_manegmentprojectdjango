from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Patient(BaseModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    patient_id = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            last_patient = Patient.objects.order_by('-id').first()
            if last_patient:
                last_id = int(last_patient.patient_id.split('-')[1])
                new_id = last_id + 1
            else:
                new_id = 1
            self.patient_id = f"PAT-{new_id:04d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.patient_id})"
    
    class Meta:
        ordering = ['-created_at']

class Doctor(BaseModel):
    SPECIALIZATION_CHOICES = [
        ('CARDIOLOGY', 'Cardiology'),
        ('NEUROLOGY', 'Neurology'),
        ('PEDIATRICS', 'Pediatrics'),
        ('ORTHOPEDICS', 'Orthopedics'),
        ('DERMATOLOGY', 'Dermatology'),
        ('GYNECOLOGY', 'Gynecology'),
        ('PSYCHIATRY', 'Psychiatry'),
        ('DENTISTRY', 'Dentistry'),
        ('OPHTHALMOLOGY', 'Ophthalmology'),
        ('GENERAL', 'General Medicine'),
    ]
    
    doctor_id = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField(help_text="Years of experience")
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.TimeField()
    available_to = models.TimeField()
    is_available = models.BooleanField(default=True)
    bio = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.doctor_id:
            last_doctor = Doctor.objects.order_by('-id').first()
            if last_doctor:
                last_id = int(last_doctor.doctor_id.split('-')[1])
                new_id = last_id + 1
            else:
                new_id = 1
            self.doctor_id = f"DOC-{new_id:04d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
    
    class Meta:
        ordering = ['specialization', 'name']

class Appointment(BaseModel):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    ]
    
    TYPE_CHOICES = [
        ('NORMAL', 'Normal'),
        ('EMERGENCY', 'Emergency'),
        ('FOLLOW_UP', 'Follow-up'),
    ]
    
    TIME_SLOTS = [
        ('09:00-10:00', '09:00 AM - 10:00 AM'),
        ('10:00-11:00', '10:00 AM - 11:00 AM'),
        ('11:00-12:00', '11:00 AM - 12:00 PM'),
        ('12:00-13:00', '12:00 PM - 01:00 PM'),
        ('14:00-15:00', '02:00 PM - 03:00 PM'),
        ('15:00-16:00', '03:00 PM - 04:00 PM'),
        ('16:00-17:00', '04:00 PM - 05:00 PM'),
    ]
    
    appointment_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='NORMAL')
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.appointment_id:
            last_appointment = Appointment.objects.order_by('-id').first()
            if last_appointment:
                last_id = int(last_appointment.appointment_id.split('-')[1])
                new_id = last_id + 1
            else:
                new_id = 1
            self.appointment_id = f"APT-{new_id:04d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.appointment_id} - {self.patient.name} with Dr. {self.doctor.name}"
    
    class Meta:
        ordering = ['date', 'time_slot']
        unique_together = ['doctor', 'date', 'time_slot']

class VisitHistory(BaseModel):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='visit_history')
    diagnosis = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    tests_recommended = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Visit for {self.appointment.patient.name} - {self.appointment.date}"
    
    class Meta:
        verbose_name_plural = "Visit Histories"
        ordering = ['-created_at']