from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Department, Room
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from medical_records.models import MedicalRecord, PrescriptionItem
from billing.models import Invoice, InvoiceItem
from datetime import date, timedelta, time
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with comprehensive, realistic hospital demo data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing Hospital Management System Seed Data..."))

        # 1. Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@hospital.org', 'admin123')
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin123)"))

        # 2. Departments
        departments_data = [
            {'name': 'Cardiology', 'code': 'CARD', 'head_of_department': 'Dr. Robert Vance', 'phone': '+1 555-0101', 'description': 'Diagnosis and treatment of congenital heart defects, coronary artery disease, and heart failure.'},
            {'name': 'Neurology', 'code': 'NEUR', 'head_of_department': 'Dr. Elena Rostova', 'phone': '+1 555-0102', 'description': 'Treatment of disorders of the nervous system, brain, and spinal cord.'},
            {'name': 'Pediatrics', 'code': 'PEDI', 'head_of_department': 'Dr. Sarah Jenkins', 'phone': '+1 555-0103', 'description': 'Comprehensive medical care for infants, children, and adolescents.'},
            {'name': 'Orthopedics', 'code': 'ORTH', 'head_of_department': 'Dr. Marcus Brody', 'phone': '+1 555-0104', 'description': 'Surgical and non-surgical treatment of conditions involving the musculoskeletal system.'},
            {'name': 'General Medicine', 'code': 'GENM', 'head_of_department': 'Dr. William Chen', 'phone': '+1 555-0105', 'description': 'Primary care and non-surgical adult healthcare management.'},
            {'name': 'Emergency Medicine', 'code': 'EMER', 'head_of_department': 'Dr. Amanda Cole', 'phone': '+1 555-0106', 'description': 'Immediate medical care for trauma, acute illnesses, and life-threatening emergencies.'},
        ]
        dept_objs = {}
        for d in departments_data:
            dept, _ = Department.objects.get_or_create(code=d['code'], defaults=d)
            dept_objs[d['code']] = dept
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(dept_objs)} Departments."))

        # 3. Rooms
        rooms_data = [
            {'room_number': '101', 'room_type': 'GENERAL', 'department': dept_objs['GENM'], 'capacity': 4, 'cost_per_day': Decimal('50.00'), 'status': 'AVAILABLE'},
            {'room_number': '102', 'room_type': 'PRIVATE', 'department': dept_objs['CARD'], 'capacity': 1, 'cost_per_day': Decimal('150.00'), 'status': 'OCCUPIED'},
            {'room_number': '201', 'room_type': 'ICU', 'department': dept_objs['EMER'], 'capacity': 2, 'cost_per_day': Decimal('350.00'), 'status': 'AVAILABLE'},
            {'room_number': '205', 'room_type': 'SEMI_PRIVATE', 'department': dept_objs['ORTH'], 'capacity': 2, 'cost_per_day': Decimal('100.00'), 'status': 'AVAILABLE'},
            {'room_number': '301', 'room_type': 'OT', 'department': dept_objs['ORTH'], 'capacity': 1, 'cost_per_day': Decimal('500.00'), 'status': 'AVAILABLE'},
        ]
        for r in rooms_data:
            Room.objects.get_or_create(room_number=r['room_number'], defaults=r)
        self.stdout.write(self.style.SUCCESS("Seeded Hospital Rooms."))

        # 4. Doctors
        doctors_data = [
            {
                'first_name': 'Robert', 'last_name': 'Vance', 'department': dept_objs['CARD'],
                'specialization': 'Interventional Cardiologist', 'qualification': 'MD, FACC',
                'experience_years': 15, 'phone': '+1 555-1001', 'email': 'r.vance@hospital.org',
                'room_number': '302A', 'consultation_fee': Decimal('150.00'),
                'available_days': 'Monday, Wednesday, Friday', 'time_slot_start': time(9, 0), 'time_slot_end': time(16, 0)
            },
            {
                'first_name': 'Elena', 'last_name': 'Rostova', 'department': dept_objs['NEUR'],
                'specialization': 'Neurosurgeon', 'qualification': 'MD, PhD',
                'experience_years': 12, 'phone': '+1 555-1002', 'email': 'e.rostova@hospital.org',
                'room_number': '410B', 'consultation_fee': Decimal('180.00'),
                'available_days': 'Tuesday, Thursday, Saturday', 'time_slot_start': time(10, 0), 'time_slot_end': time(17, 0)
            },
            {
                'first_name': 'Sarah', 'last_name': 'Jenkins', 'department': dept_objs['PEDI'],
                'specialization': 'Pediatrician', 'qualification': 'MBBS, FAAP',
                'experience_years': 8, 'phone': '+1 555-1003', 'email': 's.jenkins@hospital.org',
                'room_number': '108', 'consultation_fee': Decimal('90.00'),
                'available_days': 'Monday, Tuesday, Wednesday, Thursday, Friday', 'time_slot_start': time(8, 30), 'time_slot_end': time(15, 30)
            },
            {
                'first_name': 'Marcus', 'last_name': 'Brody', 'department': dept_objs['ORTH'],
                'specialization': 'Orthopedic Surgeon', 'qualification': 'MS (Ortho), FRCS',
                'experience_years': 14, 'phone': '+1 555-1004', 'email': 'm.brody@hospital.org',
                'room_number': '214', 'consultation_fee': Decimal('140.00'),
                'available_days': 'Monday, Wednesday, Thursday', 'time_slot_start': time(9, 0), 'time_slot_end': time(16, 30)
            },
            {
                'first_name': 'William', 'last_name': 'Chen', 'department': dept_objs['GENM'],
                'specialization': 'Internal Medicine Specialist', 'qualification': 'MD, FACP',
                'experience_years': 10, 'phone': '+1 555-1005', 'email': 'w.chen@hospital.org',
                'room_number': '104', 'consultation_fee': Decimal('80.00'),
                'available_days': 'Monday, Tuesday, Wednesday, Thursday, Friday', 'time_slot_start': time(8, 0), 'time_slot_end': time(16, 0)
            },
        ]
        doc_objs = []
        for d in doctors_data:
            doc, _ = Doctor.objects.get_or_create(email=d['email'], defaults=d)
            doc_objs.append(doc)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(doc_objs)} Doctors."))

        # 5. Patients
        patients_data = [
            {
                'first_name': 'James', 'last_name': 'Wilson', 'gender': 'M', 'date_of_birth': date(1982, 4, 15),
                'blood_group': 'O+', 'phone': '+1 555-2001', 'email': 'james.wilson@gmail.com', 'address': '742 Evergreen Terrace, Springfield',
                'emergency_contact_name': 'Emily Wilson', 'emergency_contact_phone': '+1 555-2002', 'emergency_contact_relation': 'Spouse',
                'allergies': 'Penicillin, Shellfish', 'chronic_conditions': 'Stage 1 Hypertension',
                'insurance_provider': 'BlueCross Shield', 'insurance_policy_number': 'BC-998812', 'status': 'ACTIVE'
            },
            {
                'first_name': 'Sophia', 'last_name': 'Martinez', 'gender': 'F', 'date_of_birth': date(1995, 8, 22),
                'blood_group': 'A+', 'phone': '+1 555-2003', 'email': 'sophia.m@gmail.com', 'address': '124 Maple Street, Seattle, WA',
                'emergency_contact_name': 'Carlos Martinez', 'emergency_contact_phone': '+1 555-2004', 'emergency_contact_relation': 'Father',
                'allergies': 'Latex', 'chronic_conditions': 'Asthma',
                'insurance_provider': 'Aetna Health', 'insurance_policy_number': 'AET-443321', 'status': 'ACTIVE'
            },
            {
                'first_name': 'David', 'last_name': 'Kim', 'gender': 'M', 'date_of_birth': date(1976, 12, 5),
                'blood_group': 'B+', 'phone': '+1 555-2005', 'email': 'david.kim@outlook.com', 'address': '550 Market St, San Francisco, CA',
                'emergency_contact_name': 'Hannah Kim', 'emergency_contact_phone': '+1 555-2006', 'emergency_contact_relation': 'Daughter',
                'allergies': 'None known', 'chronic_conditions': 'Type 2 Diabetes',
                'insurance_provider': 'United Healthcare', 'insurance_policy_number': 'UHC-771190', 'status': 'INPATIENT'
            },
            {
                'first_name': 'Olivia', 'last_name': 'Taylor', 'gender': 'F', 'date_of_birth': date(2017, 3, 10),
                'blood_group': 'AB+', 'phone': '+1 555-2007', 'email': 'taylor.parents@gmail.com', 'address': '89 Oak Avenue, Boston, MA',
                'emergency_contact_name': 'Jessica Taylor', 'emergency_contact_phone': '+1 555-2008', 'emergency_contact_relation': 'Mother',
                'allergies': 'Peanuts', 'chronic_conditions': 'None',
                'insurance_provider': 'Cigna Health', 'insurance_policy_number': 'CIG-120084', 'status': 'ACTIVE'
            },
            {
                'first_name': 'Alexander', 'last_name': 'Wright', 'gender': 'M', 'date_of_birth': date(1965, 11, 30),
                'blood_group': 'O-', 'phone': '+1 555-2009', 'email': 'a.wright@corp.com', 'address': '300 Pine Lane, Austin, TX',
                'emergency_contact_name': 'Margaret Wright', 'emergency_contact_phone': '+1 555-2010', 'emergency_contact_relation': 'Spouse',
                'allergies': 'Sulfa drugs', 'chronic_conditions': 'Coronary Artery Disease',
                'insurance_provider': 'Medicare Advantage', 'insurance_policy_number': 'MED-550921', 'status': 'ACTIVE'
            },
        ]
        patient_objs = []
        for p in patients_data:
            pat, _ = Patient.objects.get_or_create(phone=p['phone'], defaults=p)
            patient_objs.append(pat)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(patient_objs)} Patients."))

        # 6. Appointments
        today = date.today()
        appointments_data = [
            {
                'patient': patient_objs[0], 'doctor': doc_objs[0],
                'appointment_date': today, 'appointment_time': time(9, 30),
                'reason_for_visit': 'Routine cardiovascular checkup and ECG review',
                'status': 'SCHEDULED', 'doctor_notes': 'Patient reports occasional palpitations during exercise.'
            },
            {
                'patient': patient_objs[1], 'doctor': doc_objs[4],
                'appointment_date': today, 'appointment_time': time(11, 0),
                'reason_for_visit': 'Persistent seasonal cough and wheezing',
                'status': 'IN_PROGRESS', 'doctor_notes': 'Perform peak flow meter test and review inhaler technique.'
            },
            {
                'patient': patient_objs[2], 'doctor': doc_objs[3],
                'appointment_date': today, 'appointment_time': time(14, 0),
                'reason_for_visit': 'Right knee pain and post-surgical rehabilitation progress',
                'status': 'SCHEDULED', 'doctor_notes': 'Check knee flexion angle and prescribe physical therapy regimen.'
            },
            {
                'patient': patient_objs[3], 'doctor': doc_objs[2],
                'appointment_date': today + timedelta(days=1), 'appointment_time': time(10, 0),
                'reason_for_visit': 'Pediatric annual wellness and immunization booster',
                'status': 'SCHEDULED', 'doctor_notes': ''
            },
            {
                'patient': patient_objs[4], 'doctor': doc_objs[0],
                'appointment_date': today - timedelta(days=3), 'appointment_time': time(10, 30),
                'reason_for_visit': 'Follow-up on blood pressure control medication',
                'status': 'COMPLETED', 'doctor_notes': 'Blood pressure stabilized on Lisinopril 20mg.'
            },
        ]

        apt_objs = []
        for apt_info in appointments_data:
            apt, _ = Appointment.objects.get_or_create(
                patient=apt_info['patient'],
                doctor=apt_info['doctor'],
                appointment_date=apt_info['appointment_date'],
                appointment_time=apt_info['appointment_time'],
                defaults=apt_info
            )
            apt_objs.append(apt)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(apt_objs)} Appointments."))

        # 7. Medical Records & Prescriptions
        rec1, _ = MedicalRecord.objects.get_or_create(
            patient=patient_objs[4],
            doctor=doc_objs[0],
            appointment=apt_objs[4],
            defaults={
                'record_date': today - timedelta(days=3),
                'symptoms': 'Occasional lightheadedness upon standing, elevated BP readings at home (145/92).',
                'diagnosis': 'Essential Hypertension (Well-Managed)',
                'treatment_plan': 'Adjust daily dosage of ACE inhibitor. Increase aerobic exercise and adhere to low-sodium diet.',
                'blood_pressure': '128/82',
                'heart_rate': 72,
                'temperature': Decimal('36.8'),
                'weight_kg': Decimal('84.5'),
                'notes': 'Repeat lipid panel and kidney function tests in 3 months.'
            }
        )
        PrescriptionItem.objects.get_or_create(
            medical_record=rec1, medication_name='Lisinopril',
            defaults={'dosage': '20mg', 'frequency': 'Once daily in morning', 'duration_days': 90, 'instructions': 'Take with or without food. Monitor blood pressure.'}
        )
        PrescriptionItem.objects.get_or_create(
            medical_record=rec1, medication_name='Amlodipine',
            defaults={'dosage': '5mg', 'frequency': 'Once daily in evening', 'duration_days': 90, 'instructions': 'Check ankles for swelling.'}
        )

        rec2, _ = MedicalRecord.objects.get_or_create(
            patient=patient_objs[1],
            doctor=doc_objs[4],
            appointment=apt_objs[1],
            defaults={
                'record_date': today,
                'symptoms': 'Dry cough for 2 weeks, chest tightness triggered by cold weather.',
                'diagnosis': 'Moderate Bronchial Asthma Exacerbation',
                'treatment_plan': 'Short course of inhaled corticosteroid + bronchodilator. Avoid known triggers.',
                'blood_pressure': '118/76',
                'heart_rate': 78,
                'temperature': Decimal('37.1'),
                'weight_kg': Decimal('62.0'),
                'notes': 'Spirometry shows 18% improvement post-albuterol.'
            }
        )
        PrescriptionItem.objects.get_or_create(
            medical_record=rec2, medication_name='Albuterol Inhaler (Ventolin)',
            defaults={'dosage': '90mcg/puff', 'frequency': '2 puffs every 4-6 hours PRN', 'duration_days': 30, 'instructions': 'Rinse mouth after use.'}
        )
        PrescriptionItem.objects.get_or_create(
            medical_record=rec2, medication_name='Fluticasone Propionate',
            defaults={'dosage': '110mcg', 'frequency': '2 puffs twice daily', 'duration_days': 60, 'instructions': 'Maintenance preventer inhaler.'}
        )
        self.stdout.write(self.style.SUCCESS("Seeded Medical Examination Records & Prescriptions."))

        # 8. Billing & Invoices
        inv1, _ = Invoice.objects.get_or_create(
            patient=patient_objs[4],
            appointment=apt_objs[4],
            defaults={
                'issue_date': today - timedelta(days=3),
                'due_date': today + timedelta(days=27),
                'subtotal': Decimal('220.00'),
                'discount': Decimal('20.00'),
                'tax': Decimal('10.00'),
                'total_amount': Decimal('210.00'),
                'paid_amount': Decimal('210.00'),
                'payment_status': 'PAID',
                'payment_method': 'CREDIT_CARD',
                'notes': 'Card ending in 4118 approved.'
            }
        )
        InvoiceItem.objects.get_or_create(invoice=inv1, description='Specialist Consultation (Cardiology)', defaults={'unit_price': Decimal('150.00'), 'quantity': 1, 'total': Decimal('150.00')})
        InvoiceItem.objects.get_or_create(invoice=inv1, description='12-Lead Electrocardiogram (ECG)', defaults={'unit_price': Decimal('70.00'), 'quantity': 1, 'total': Decimal('70.00')})

        inv2, _ = Invoice.objects.get_or_create(
            patient=patient_objs[0],
            appointment=apt_objs[0],
            defaults={
                'issue_date': today,
                'due_date': today + timedelta(days=14),
                'subtotal': Decimal('150.00'),
                'discount': Decimal('0.00'),
                'tax': Decimal('7.50'),
                'total_amount': Decimal('157.50'),
                'paid_amount': Decimal('0.00'),
                'payment_status': 'PENDING',
                'payment_method': 'INSURANCE',
                'notes': 'Claim pre-authorized under BlueCross Shield.'
            }
        )
        InvoiceItem.objects.get_or_create(invoice=inv2, description='Doctor Consultation - Cardiology', defaults={'unit_price': Decimal('150.00'), 'quantity': 1, 'total': Decimal('150.00')})

        self.stdout.write(self.style.SUCCESS("Seeded Invoices and Billing line items."))
        self.stdout.write(self.style.SUCCESS("=== Hospital Management System Data Seed Completed Successfully! ==="))

