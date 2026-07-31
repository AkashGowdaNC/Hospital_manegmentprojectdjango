from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
import json
import logging

logger = logging.getLogger(__name__)

from .models import Patient, Doctor, Appointment, VisitHistory
from .forms import PatientForm, DoctorForm, AppointmentForm, VisitHistoryForm

# Dashboard View
def dashboard(request):
    try:
        # Real data calculations
        total_patients = Patient.objects.count()
        total_doctors = Doctor.objects.filter(is_available=True).count()
        
        # Today's appointments
        today = timezone.now().date()
        today_appointments = Appointment.objects.filter(date=today).count()
        
        # Emergency cases (today)
        emergency_cases = Appointment.objects.filter(
            appointment_type='EMERGENCY', 
            date=today,
            status='SCHEDULED'
        ).count()
        
        # Recent appointments (last 5)
        recent_appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-created_at')[:5]
        
        # Appointment trends (last 7 days)
        seven_days_ago = today - timedelta(days=6)
        appointment_trends = []
        date_labels = []
        
        for i in range(7):
            current_date = seven_days_ago + timedelta(days=i)
            count = Appointment.objects.filter(date=current_date).count()
            appointment_trends.append(count)
            date_labels.append(current_date.strftime('%a'))
        
        # Doctor distribution by specialization
        doctor_distribution = Doctor.objects.values('specialization').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Prepare data for charts
        specialization_labels = [doc['specialization'] for doc in doctor_distribution]
        specialization_data = [doc['count'] for doc in doctor_distribution]
        
        # System status data
        total_appointments = Appointment.objects.count()
        completed_appointments = Appointment.objects.filter(status='COMPLETED').count()
        pending_appointments = Appointment.objects.filter(status='SCHEDULED').count()
        
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error in dashboard view: {str(e)}", exc_info=True)
        # Fallback data in case of errors
        total_patients = 0
        total_doctors = 0
        today_appointments = 0
        emergency_cases = 0
        recent_appointments = []
        appointment_trends = [0, 0, 0, 0, 0, 0, 0]
        date_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        specialization_labels = []
        specialization_data = []
        total_appointments = 0
        completed_appointments = 0
        pending_appointments = 0
    
    context = {
        'page_title': 'Dashboard',
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'today_appointments': today_appointments,
        'emergency_cases': emergency_cases,
        'recent_appointments': recent_appointments,
        'appointment_trends': json.dumps(appointment_trends),
        'date_labels': json.dumps(date_labels),
        'specialization_labels': json.dumps(specialization_labels),
        'specialization_labels_list': specialization_labels,  # Raw list for template use
        'specialization_data': json.dumps(specialization_data),
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'pending_appointments': pending_appointments,
    }
    return render(request, 'core/dashboard.html', context)

# Patient CRUD Views
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        patients = patients.filter(
            Q(name__icontains=search_query) |
            Q(patient_id__icontains=search_query) |
            Q(contact_number__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(patients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Patients',
        'page_obj': page_obj,
        'search_query': search_query,
        'total_patients': patients.count(),
    }
    return render(request, 'core/patients/list.html', context)

def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient {patient.name} created successfully!')
            return redirect('patient_list')
    else:
        form = PatientForm()
    
    context = {
        'page_title': 'Add New Patient',
        'form': form,
    }
    return render(request, 'core/patients/form.html', context)

def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.all().order_by('-date')
    context = {
        'page_title': f'Patient - {patient.name}',
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'core/patients/detail.html', context)

def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient {patient.name} updated successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    
    context = {
        'page_title': f'Update Patient - {patient.name}',
        'form': form,
        'patient': patient,
    }
    return render(request, 'core/patients/form.html', context)

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient_name = patient.name
        patient.delete()
        messages.success(request, f'Patient {patient_name} deleted successfully!')
        return redirect('patient_list')
    
    context = {
        'page_title': 'Delete Patient',
        'patient': patient,
    }
    return render(request, 'core/patients/delete.html', context)

# Doctor CRUD Views
def doctor_list(request):
    doctors = Doctor.objects.all().order_by('specialization', 'name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        doctors = doctors.filter(
            Q(name__icontains=search_query) |
            Q(doctor_id__icontains=search_query) |
            Q(specialization__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(doctors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Doctors',
        'page_obj': page_obj,
        'search_query': search_query,
        'total_doctors': doctors.count(),
    }
    return render(request, 'core/doctors/list.html', context)

def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f'Dr. {doctor.name} created successfully!')
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    
    context = {
        'page_title': 'Add New Doctor',
        'form': form,
    }
    return render(request, 'core/doctors/form.html', context)

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    appointments = doctor.appointments.filter(date__gte=timezone.now().date()).order_by('date', 'time_slot')
    context = {
        'page_title': f'Doctor - {doctor.name}',
        'doctor': doctor,
        'appointments': appointments,
    }
    return render(request, 'core/doctors/detail.html', context)

def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f'Dr. {doctor.name} updated successfully!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    
    context = {
        'page_title': f'Update Doctor - {doctor.name}',
        'form': form,
        'doctor': doctor,
    }
    return render(request, 'core/doctors/form.html', context)

def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor_name = doctor.name
        doctor.delete()
        messages.success(request, f'Dr. {doctor_name} deleted successfully!')
        return redirect('doctor_list')
    
    context = {
        'page_title': 'Delete Doctor',
        'doctor': doctor,
    }
    return render(request, 'core/doctors/delete.html', context)

# Appointment CRUD Views
def appointment_list(request):
    appointments = Appointment.objects.select_related('patient', 'doctor').all().order_by('-date', '-created_at')
    
    # Filter functionality
    status_filter = request.GET.get('status', '')
    doctor_filter = request.GET.get('doctor', '')
    date_filter = request.GET.get('date', '')
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    if doctor_filter:
        appointments = appointments.filter(doctor_id=doctor_filter)
    if date_filter:
        appointments = appointments.filter(date=date_filter)
    
    # Pagination
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    doctors = Doctor.objects.all()
    
    context = {
        'page_title': 'Appointments',
        'page_obj': page_obj,
        'doctors': doctors,
        'status_filter': status_filter,
        'doctor_filter': doctor_filter,
        'date_filter': date_filter,
        'total_appointments': appointments.count(),
    }
    return render(request, 'core/appointments/list.html', context)

def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f'Appointment {appointment.appointment_id} created successfully!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    
    context = {
        'page_title': 'Book New Appointment',
        'form': form,
    }
    return render(request, 'core/appointments/form.html', context)

def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    visit_history = getattr(appointment, 'visit_history', None)
    
    if request.method == 'POST' and 'update_status' in request.POST:
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Appointment status updated to {new_status}')
            return redirect('appointment_detail', pk=appointment.pk)
    
    context = {
        'page_title': f'Appointment - {appointment.appointment_id}',
        'appointment': appointment,
        'visit_history': visit_history,
    }
    return render(request, 'core/appointments/detail.html', context)

def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f'Appointment {appointment.appointment_id} updated successfully!')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    
    context = {
        'page_title': f'Update Appointment - {appointment.appointment_id}',
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'core/appointments/form.html', context)

def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment_id = appointment.appointment_id
        appointment.delete()
        messages.success(request, f'Appointment {appointment_id} deleted successfully!')
        return redirect('appointment_list')
    
    context = {
        'page_title': 'Delete Appointment',
        'appointment': appointment,
    }
    return render(request, 'core/appointments/delete.html', context)

# API Views
def doctor_available_slots(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    date = request.GET.get('date')
    
    if not date:
        return JsonResponse({'error': 'Date parameter is required'}, status=400)
    
    # Get booked slots for the doctor on the given date
    booked_slots = Appointment.objects.filter(
        doctor=doctor,
        date=date,
        status__in=['SCHEDULED', 'COMPLETED']
    ).values_list('time_slot', flat=True)
    
    # All possible time slots
    all_slots = [choice[0] for choice in Appointment.TIME_SLOTS]
    
    # Available slots (not booked)
    available_slots = [slot for slot in all_slots if slot not in booked_slots]
    
    return JsonResponse({
        'doctor_id': doctor.id,
        'date': date,
        'available_slots': available_slots,
        'booked_slots': list(booked_slots)
    })
def login_view(request):
    return render(request, 'core/login.html')