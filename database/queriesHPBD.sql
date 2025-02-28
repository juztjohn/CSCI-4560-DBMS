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
-- adding data
INSERT INTO USER_ACCOUNTS (User_id, User_name, User_phone, User_email) VALUES
('P00000006', 'Alice McDonald', '556-173-9567', 'aliceM@example.com');

-- update data
UPDATE RECORDS SET Treatment_notes = 'Rest, hydration, and vitamin C' WHERE Patient_id = 'P00000001';

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


