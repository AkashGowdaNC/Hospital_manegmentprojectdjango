@echo off
echo Checking Hospital Database...
python -c "
import sqlite3
import os

if os.path.exists('db.sqlite3'):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    
    # Count records
    c.execute('SELECT COUNT(*) FROM core_patient')
    patients = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM core_doctor')
    doctors = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM core_appointment') 
    appointments = c.fetchone()[0]
    
    print('=== DATABASE STATS ===')
    print(f'Patients: {patients}')
    print(f'Doctors: {doctors}')
    print(f'Appointments: {appointments}')
    print('======================')
    
    conn.close()
else:
    print('Database file not found!')
"
pause