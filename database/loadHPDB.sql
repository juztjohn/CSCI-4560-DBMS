-- loadHPDB.sql load the database with the initial data

-- Use the correct database
USE healthPortalDB;

-- Insert User Accounts (starting at ID 100)
INSERT INTO USER_ACCOUNTS (Status, User_name, User_phone, User_email, Password, DOB) VALUES
('Patient', 'John Doe', '123-456-7890', 'johndoe@example.com', 'Pass1234', '01/01/2000'),
('Patient', 'Jane Smith', '987-654-3210', 'janesmith@example.com', 'Secure456', '03/01/2003'),
('Patient', 'Alice Brown', '555-555-5555', 'alicebrown@example.com', 'Alice789', '05/01/2007'),
('Doctor', 'Dr. Emily White', '111-222-3333', 'drwhite@example.com', 'DrWhite99', '07/01/1990'),
('Doctor', 'Dr. Robert Black', '222-333-4444', 'drblack@example.com', 'BlackDoc12', '09/01/1980');

-- Insert Medical Records (Using corresponding User IDs)
INSERT INTO RECORDS (Patient_id, Patient_name, Diagnosis, Treatment_notes, Prescription, Blood_type) VALUES
(100, 'John Doe', 'Flu', 'Rest and hydration', 'Tamiflu', 'O+'),
(101, 'Jane Smith', 'Hypertension', 'Monitor blood pressure', 'Lisinopril', 'A-'),
(102, 'Alice Brown', 'Diabetes', 'Maintain diet and exercise', 'Metformin', 'B+');

-- Insert Doctors (Using corresponding User IDs)
INSERT INTO DOCTOR (Dr_id, Dr_name, Dr_phone, Dr_email, Facility_addr) VALUES
(103, 'Dr. Emily White', '111-222-3333', 'drwhite@example.com', 'City Hospital'),
(104, 'Dr. Robert Black', '222-333-4444', 'drblack@example.com', 'Downtown Clinic');

-- Insert Appointments (Ensure Patients and Doctors Exist)
INSERT INTO APPOINTMENTS (Patient_id, Dr_id, Date, Time, Appt_type, Facility_addr) VALUES
(100, 103, '2025-04-10', '10:00 AM', 'General Checkup', 'City Hospital'),
(101, 104, '2025-04-12', '02:00 PM', 'Follow-up', 'Downtown Clinic');

-- Insert Billing Information
INSERT INTO BILLING (User_id, Amount, Insurance, Payment_status) VALUES
(100, 150.00, 'BlueShield', TRUE),
(101, 200.00, 'Medicare', FALSE),
(102, 100.00, 'Private', TRUE);
