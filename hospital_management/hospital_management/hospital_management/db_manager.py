import sqlite3
import os
from datetime import datetime

def show_database_stats():
    """Show database statistics and contents"""
    if not os.path.exists('db.sqlite3'):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    print("🔍 Database Statistics")
    print("=" * 50)
    
    # Get table information
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"📊 Total Tables: {len(tables)}")
    print("\n📋 Table Details:")
    print("-" * 30)
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   {table_name}: {count} records")
    
    # Show sample data from main tables
    print("\n👥 Sample Data:")
    print("-" * 30)
    
    # Patients sample
    cursor.execute("SELECT patient_id, name, age, gender FROM core_patient LIMIT 5")
    patients = cursor.fetchall()
    print(f"👤 Recent Patients (showing {len(patients)}):")
    for patient in patients:
        print(f"   {patient[0]} - {patient[1]} ({patient[2]} yrs, {patient[3]})")
    
    # Doctors sample  
    cursor.execute("SELECT doctor_id, name, specialization FROM core_doctor LIMIT 5")
    doctors = cursor.fetchall()
    print(f"\n👨‍⚕️ Doctors (showing {len(doctors)}):")
    for doctor in doctors:
        print(f"   {doctor[0]} - Dr. {doctor[1]} ({doctor[2]})")
    
    # Appointments sample
    cursor.execute("""
        SELECT a.appointment_id, p.name, d.name, a.date, a.status 
        FROM core_appointment a
        JOIN core_patient p ON a.patient_id = p.id
        JOIN core_doctor d ON a.doctor_id = d.id
        LIMIT 5
    """)
    appointments = cursor.fetchall()
    print(f"\n📅 Recent Appointments (showing {len(appointments)}):")
    for apt in appointments:
        print(f"   {apt[0]} - {apt[1]} with Dr. {apt[2]} on {apt[3]} ({apt[4]})")
    
    conn.close()

def backup_database():
    """Create a backup of the database"""
    if not os.path.exists('db.sqlite3'):
        print("❌ Database file not found!")
        return
    
    # Create backups directory
    if not os.path.exists('backups'):
        os.makedirs('backups')
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = f"backups/db_backup_{timestamp}.sqlite3"
    
    # Copy database file
    import shutil
    shutil.copy2('db.sqlite3', backup_file)
    
    print(f"✅ Backup created: {backup_file}")
    
    # Show backup size
    size_kb = os.path.getsize(backup_file) / 1024
    print(f"📦 Backup size: {size_kb:.1f} KB")

def list_backups():
    """List all available backups"""
    if not os.path.exists('backups'):
        print("❌ No backups directory found!")
        return
    
    backups = [f for f in os.listdir('backups') if f.endswith('.sqlite3')]
    backups.sort(reverse=True)
    
    if not backups:
        print("❌ No backup files found!")
        return
    
    print(f"📁 Available Backups ({len(backups)}):")
    print("-" * 40)
    
    for backup in backups[:10]:  # Show last 10 backups
        backup_path = os.path.join('backups', backup)
        size_kb = os.path.getsize(backup_path) / 1024
        print(f"   {backup} ({size_kb:.1f} KB)")
    
    if len(backups) > 10:
        print(f"   ... and {len(backups) - 10} more")

def restore_backup():
    """Restore database from backup"""
    list_backups()
    
    backup_files = [f for f in os.listdir('backups') if f.endswith('.sqlite3')]
    if not backup_files:
        print("❌ No backup files available!")
        return
    
    print(f"\n🔄 Available backups:")
    for i, backup in enumerate(backup_files[:10], 1):
        print(f"   {i}. {backup}")
    
    try:
        choice = int(input(f"\nEnter backup number to restore (1-{len(backup_files[:10])}): "))
        if 1 <= choice <= len(backup_files[:10]):
            selected_backup = backup_files[choice-1]
            
            # Create pre-restore backup
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            pre_restore = f"backups/pre_restore_{timestamp}.sqlite3"
            import shutil
            shutil.copy2('db.sqlite3', pre_restore)
            
            # Restore selected backup
            shutil.copy2(f"backups/{selected_backup}", 'db.sqlite3')
            
            print(f"✅ Database restored from: {selected_backup}")
            print(f"💾 Pre-restore backup saved as: {pre_restore}")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a valid number!")

def export_to_csv():
    """Export data to CSV files"""
    if not os.path.exists('db.sqlite3'):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Create exports directory
    if not os.path.exists('exports'):
        os.makedirs('exports')
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Export patients
    cursor.execute("SELECT * FROM core_patient")
    patients = cursor.fetchall()
    
    if patients:
        with open(f'exports/patients_{timestamp}.csv', 'w', newline='', encoding='utf-8') as f:
            import csv
            writer = csv.writer(f)
            # Write header
            writer.writerow(['ID', 'Patient ID', 'Name', 'Age', 'Gender', 'Contact', 'Email', 'Address', 'Emergency Contact', 'Blood Group', 'Created At'])
            # Write data
            writer.writerows(patients)
        print(f"✅ Patients exported: exports/patients_{timestamp}.csv")
    
    # Export doctors
    cursor.execute("SELECT * FROM core_doctor")
    doctors = cursor.fetchall()
    
    if doctors:
        with open(f'exports/doctors_{timestamp}.csv', 'w', newline='', encoding='utf-8') as f:
            import csv
            writer = csv.writer(f)
            writer.writerow(['ID', 'Doctor ID', 'Name', 'Specialization', 'Qualification', 'Experience', 'Contact', 'Email', 'Consultation Fee', 'Available From', 'Available To', 'Is Available', 'Bio', 'Created At'])
            writer.writerows(doctors)
        print(f"✅ Doctors exported: exports/doctors_{timestamp}.csv")
    
    # Export appointments
    cursor.execute("""
        SELECT a.*, p.name as patient_name, p.patient_id, d.name as doctor_name, d.doctor_id
        FROM core_appointment a
        JOIN core_patient p ON a.patient_id = p.id
        JOIN core_doctor d ON a.doctor_id = d.id
    """)
    appointments = cursor.fetchall()
    
    if appointments:
        with open(f'exports/appointments_{timestamp}.csv', 'w', newline='', encoding='utf-8') as f:
            import csv
            writer = csv.writer(f)
            writer.writerow(['ID', 'Appointment ID', 'Patient ID', 'Doctor ID', 'Date', 'Time Slot', 'Status', 'Type', 'Reason', 'Notes', 'Created At', 'Updated At', 'Patient Name', 'Doctor Name'])
            writer.writerows(appointments)
        print(f"✅ Appointments exported: exports/appointments_{timestamp}.csv")
    
    conn.close()

def main():
    """Main menu for database management"""
    while True:
        print("\n" + "="*60)
        print("🏥 CLOVER HOSPITAL - DATABASE MANAGEMENT")
        print("="*60)
        print("1. 📊 Show Database Statistics")
        print("2. 💾 Create Database Backup") 
        print("3. 📁 List Available Backups")
        print("4. 🔄 Restore from Backup")
        print("5. 📤 Export Data to CSV")
        print("6. 🚪 Exit")
        print("-"*60)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            show_database_stats()
        elif choice == '2':
            backup_database()
        elif choice == '3':
            list_backups()
        elif choice == '4':
            restore_backup()
        elif choice == '5':
            export_to_csv()
        elif choice == '6':
            print("👋 Goodbye! Thank you for using Clover Hospital System!")
            break
        else:
            print("❌ Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()