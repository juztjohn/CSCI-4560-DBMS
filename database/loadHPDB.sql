-- loadHPDB.sql load the database with the initial data

-- Use the correct database
USE healthPortalDB;

-- Insert Users
INSERT INTO USER_ACCOUNTS (User_id, User_name, User_phone, User_email) VALUES
('P00000001', 'Alice Johnson', '555-123-4567', 'alice@example.com'),
('P00000002', 'Bob Smith', '555-234-5678', 'bob@example.com'),
('P00000003', 'Charlie Brown', '555-345-6789', 'charlie@example.com'),
('P00000004', 'Diana Prince', '555-456-7890', 'diana@example.com'),
('P00000005', 'Ethan Hunt', '555-567-8901', 'ethan@example.com');

-- Insert Patients
INSERT INTO RECORDS (Patient_id, Patient_name, Diagnosis, Treatment_notes, Prescription, Blood_type) VALUES
('P00000001', 'Alice Johnson', 'Flu', 'Rest and hydration', 'Tamiflu', 'O+'),
('P00000002', 'Bob Smith', 'Diabetes', 'Monitor blood sugar', 'Insulin', 'A-'),
('P00000003', 'Charlie Brown', 'Hypertension', 'Reduce salt intake', 'Lisinopril', 'B+'),
('P00000004', 'Diana Prince', 'Asthma', 'Use inhaler as needed', 'Albuterol', 'AB-'),
('P00000005', 'Ethan Hunt', 'Migraine', 'Avoid bright lights', 'Sumatriptan', 'O-');

-- Insert Doctors
INSERT INTO DOCTOR (Dr_id, Dr_name, Dr_phone, Dr_email, Facility_addr) VALUES
('D00000001', 'Dr. John Doe', '555-111-2222', 'dr.johndoe@example.com', '123 Health St'),
('D00000002', 'Dr. Emily White', '555-222-3333', 'dr.emily@example.com', '456 Care Ave'),
('D00000003', 'Dr. Mike Green', '555-333-4444', 'dr.mike@example.com', '789 Wellness Blvd');

-- Insert Appointments
INSERT INTO APPOINTMENTS (Patient_id, Dr_id, Date, Time, Appt_type, Facility_addr) VALUES
('P00000001', 'D00000001', '2025-03-01', '09:00:00', 'General Checkup', '123 Health St'),
('P00000002', 'D00000002', '2025-03-02', '10:30:00', 'Diabetes Consultation', '456 Care Ave'),
('P00000003', 'D00000003', '2025-03-03', '14:00:00', 'Blood Pressure Check', '789 Wellness Blvd'),
('P00000004', 'D00000001', '2025-03-04', '15:45:00', 'Asthma Follow-up', '123 Health St'),
('P00000005', 'D00000002', '2025-03-05', '08:15:00', 'Migraine Treatment', '456 Care Ave');

-- Insert Billing Records
INSERT INTO BILLING (User_id, Amount, Insurance, Payment_status) VALUES
('P00000001', 200.50, 'BlueCross', TRUE),
('P00000002', 150.75, 'Aetna', FALSE),
('P00000003', 300.00, 'UnitedHealth', TRUE),
('P00000004', 400.25, 'Medicare', TRUE),
('P00000005', 100.00, 'Cigna', FALSE);
