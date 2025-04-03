-- queriesHPDB.sql contains the queries for the db

-- user database
USE healthPortalDB;

-- show all tables
SELECT *
FROM USER_ACCOUNTS;

SELECT *
FROM RECORDS;

SELECT *
FROM DOCTOR;

SELECT *
FROM APPOINTMENTS;

SELECT *
FROM BILLING;

-- basic queries
-- adding user
	-- upon first login, get name,phone,email,and most importantly pass and status
INSERT INTO USER_ACCOUNTS (Status, User_name, User_phone, User_email, Password) VALUES
('Admin', 'admin name', '876-456-7890', 'admin@example.com', 'Password');

-- update user
-- update user status
UPDATE USER_ACCOUNTS SET Status = 'Patient' WHERE User_id = 104;
-- update user name
UPDATE USER_ACCOUNTS SET User_name = 'Robert Black' WHERE User_id = 104;
-- update user phone
UPDATE USER_ACCOUNTS SET User_phone = '333-333-4444' WHERE User_id = 104;
-- update user email
UPDATE USER_ACCOUNTS SET User_email = 'robbie@example.org' WHERE User_id = 104;
-- update user pass
UPDATE USER_ACCOUNTS SET Password = 'NewPass' WHERE User_id = 104;

-- update patient data
-- update patient notes
UPDATE RECORDS SET Treatment_notes = 'Rest, hydration, and vitamin C' WHERE Patient_id = 101;
-- update patient diagnosis
UPDATE RECORDS SET Diagnosis = 'Common Flu' WHERE Patient_id = 101;
-- update prescription
UPDATE RECORDS SET Prescription = 'None' WHERE Patient_id = 101;


-- example uses of database UNFINISHED CODE

-- all users
-- view user account info
SELECT * FROM USER_ACCOUNTS WHERE User_id = ?;

-- update accnt info
UPDATE USER_ACCOUNTS 
SET User_phone = '999-888-7777' 
WHERE User_id = ?;


-- Patient Uses
-- view their appts
SELECT A.Date, A.Time, A.Appt_type, A.Facility_addr, D.Dr_name 
FROM APPOINTMENTS A 
JOIN DOCTOR D ON A.Dr_id = D.Dr_id
WHERE A.Patient_id = ?;

-- view their diagnosis, treatement, prescription
SELECT Diagnosis, Treatment_notes, Prescription 
FROM RECORDS 
WHERE Patient_id = ?;

-- view all personal records
SELECT * FROM RECORDS WHERE Patient_id = ?;

-- view bills
SELECT * FROM BILLING WHERE User_id = ?;

-- pay bills
UPDATE BILLING 
SET Payment_status = TRUE 
WHERE User_id = ?;

-- view/add notes
SELECT Notes FROM RECORDS WHERE Patient_id = ?;


-- doctor/nurse uses
-- view its patients appts
SELECT A.Date, A.Time, A.Appt_type, A.Facility_addr, P.Patient_name 
FROM APPOINTMENTS A
JOIN RECORDS P ON A.Patient_id = P.Patient_id
WHERE A.Dr_id = ?;

-- view diagnosis, treatement, prescription for patients
SELECT Patient_name, Diagnosis, Treatment_notes, Prescription 
FROM RECORDS;

-- view/add notes
SELECT Patient_name, Notes FROM RECORDS;

UPDATE RECORDS 
SET Notes = CONCAT(Notes, ' Doctor update: new observation.') 
WHERE Patient_id = ?;


-- receptionist uses
-- view all appts
SELECT A.Date, A.Time, A.Appt_type, A.Facility_addr, 
       P.Patient_name, D.Dr_name 
FROM APPOINTMENTS A
JOIN RECORDS P ON A.Patient_id = P.Patient_id
JOIN DOCTOR D ON A.Dr_id = D.Dr_id;

-- add appts via patients' and doctors' DOB and name
INSERT INTO APPOINTMENTS (Patient_id, Dr_id, Date, Time, Appt_type, Facility_addr)
SELECT UA1.User_id, UA2.User_id, '2025-04-15', '11:00 AM', 'Consultation', 'City Hospital'
FROM USER_ACCOUNTS UA1, USER_ACCOUNTS UA2
WHERE UA1.User_name = 'John Doe' AND UA1.DOB = '1990-01-01'
AND UA2.User_name = 'Dr. Emily White' AND UA2.DOB = '1975-05-10';

-- modify appts
UPDATE APPOINTMENTS 
SET Time = '03:00 PM' 
WHERE Patient_id = ? AND Dr_id = ? AND Date = '2025-04-15';

-- delete appts
DELETE FROM APPOINTMENTS 
WHERE Patient_id = ? AND Dr_id = ? AND Date = '2025-04-15';

-- view list of doctors
SELECT * FROM DOCTOR;


-- admin uses
-- get all users
SELECT * FROM USER_ACCOUNTS;

-- sort
SELECT * FROM RECORDS WHERE Diagnosis = 'Flu';

-- more complex
-- gets all appts and their doctor and patients info
SELECT A.Date, A.Time, A.Appt_type, 
       P.Patient_name, P.Diagnosis, P.Blood_type,
       D.Dr_name, D.Facility_addr
FROM APPOINTMENTS A
JOIN RECORDS P ON A.Patient_id = P.Patient_id
JOIN DOCTOR D ON A.Dr_id = D.Dr_id
ORDER BY A.Date, A.Time;

-- get all patient outstanding bills
SELECT U.User_name, B.Amount, B.Insurance
FROM BILLING B
JOIN USER_ACCOUNTS U ON B.User_id = U.User_id
WHERE B.Payment_status = FALSE
ORDER BY B.Amount DESC;

