from django.contrib import admin
from django.utils.html import format_html
from .models import Patient, Doctor, Appointment, VisitHistory

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'name', 'age', 'gender', 'contact_number', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('name', 'patient_id', 'contact_number')
    readonly_fields = ('patient_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('patient_id', 'name', 'age', 'gender', 'blood_group')
        }),
        ('Contact Information', {
            'fields': ('contact_number', 'email', 'address', 'emergency_contact')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'allergies')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'name', 'specialization', 'experience', 'consultation_fee', 'is_available_display')
    list_filter = ('specialization', 'is_available', 'created_at')
    search_fields = ('name', 'doctor_id', 'specialization')
    readonly_fields = ('doctor_id', 'created_at', 'updated_at')
    
    def is_available_display(self, obj):
        if obj.is_available:
            return format_html('<span style="color: green;">● Available</span>')
        return format_html('<span style="color: red;">● Not Available</span>')
    is_available_display.short_description = 'Availability'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('doctor_id', 'name', 'specialization', 'qualification')
        }),
        ('Professional Details', {
            'fields': ('experience', 'consultation_fee', 'available_from', 'available_to', 'is_available')
        }),
        ('Contact Information', {
            'fields': ('contact_number', 'email', 'bio')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient_name', 'doctor_name', 'date', 'time_slot', 'status_display', 'type_display')
    list_filter = ('status', 'appointment_type', 'date', 'doctor')
    search_fields = ('appointment_id', 'patient__name', 'doctor__name')
    readonly_fields = ('appointment_id', 'created_at', 'updated_at')
    
    def patient_name(self, obj):
        return obj.patient.name
    patient_name.short_description = 'Patient'
    
    def doctor_name(self, obj):
        return f"Dr. {obj.doctor.name}"
    doctor_name.short_description = 'Doctor'
    
    def status_display(self, obj):
        color_map = {
            'SCHEDULED': 'orange',
            'COMPLETED': 'green',
            'CANCELLED': 'red',
            'NO_SHOW': 'gray',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            color_map.get(obj.status, 'black'),
            obj.status
        )
    status_display.short_description = 'Status'
    
    def type_display(self, obj):
        if obj.appointment_type == 'EMERGENCY':
            return format_html('<span style="color: red; font-weight: bold;">🚨 {}</span>', obj.appointment_type)
        return obj.appointment_type
    type_display.short_description = 'Type'
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('appointment_id', 'patient', 'doctor', 'date', 'time_slot')
        }),
        ('Additional Information', {
            'fields': ('status', 'appointment_type', 'reason', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(VisitHistory)
class VisitHistoryAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'diagnosis_preview', 'follow_up_date', 'created_at')
    list_filter = ('follow_up_date', 'created_at')
    search_fields = ('appointment__patient__name', 'diagnosis')
    readonly_fields = ('created_at', 'updated_at')
    
    def diagnosis_preview(self, obj):
        if obj.diagnosis:
            return obj.diagnosis[:50] + '...' if len(obj.diagnosis) > 50 else obj.diagnosis
        return "No diagnosis recorded"
    diagnosis_preview.short_description = 'Diagnosis'
    
    fieldsets = (
        ('Appointment Reference', {
            'fields': ('appointment',)
        }),
        ('Medical Details', {
            'fields': ('symptoms', 'diagnosis', 'prescription', 'tests_recommended')
        }),
        ('Follow-up', {
            'fields': ('follow_up_date', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )