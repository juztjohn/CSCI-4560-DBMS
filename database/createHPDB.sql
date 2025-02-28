-- CreateDB.sql file
-- creates the relations

-- Create the database
CREATE DATABASE IF NOT EXISTS healthPortalDB;

-- Set to use
USE healthPortalDB;

-- User Accounts Table
CREATE TABLE USER_ACCOUNTS (
	User_id CHAR(9) NOT NULL,
	User_name VARCHAR(30) NOT NULL,
    User_phone CHAR(12),
	User_email VARCHAR(30),
	PRIMARY KEY(User_id)
);

-- Medical Records Table
CREATE TABLE RECORDS (
	Patient_id CHAR(9) NOT NULL,
	Patient_name VARCHAR(30) NOT NULL,
    Diagnosis VARCHAR(30) NOT NULL,
    Treatment_notes VARCHAR(30) NOT NULL,
    Prescription VARCHAR(30) NOT NULL,
    Blood_type VARCHAR(30) NOT NULL,
	PRIMARY KEY(Patient_id)
);

-- Doctors Table
CREATE TABLE DOCTOR (
	Dr_id CHAR(9) NOT NULL,
    Dr_name VARCHAR(30) NOT NULL,
    Dr_phone CHAR(12),
	Dr_email VARCHAR(30),
    Facility_addr VARCHAR(30),
	PRIMARY KEY(Dr_id)
);

-- Appointments Table with Foreign Keys
CREATE TABLE APPOINTMENTS (
	Patient_id CHAR(9) NOT NULL,
    Dr_id CHAR(9) NOT NULL,
    Date CHAR(10),
    Time CHAR(8),
    Appt_type VARCHAR(30),
    Facility_addr VARCHAR(30),
    PRIMARY KEY (Patient_id, Dr_id, Date, Time), -- Ensuring uniqueness of each appointment
    FOREIGN KEY (Patient_id) REFERENCES RECORDS(Patient_id) ON DELETE CASCADE,
    FOREIGN KEY (Dr_id) REFERENCES DOCTOR(Dr_id) ON DELETE CASCADE
);

-- Billing Table with Foreign Key & Decimal Fix
CREATE TABLE BILLING (
	User_id CHAR(9) NOT NULL,
    Amount DECIMAL(10,2) NOT NULL, -- Fixing decimal precision
    Insurance VARCHAR(30),
    Payment_status BOOL DEFAULT FALSE,
    PRIMARY KEY (User_id), 
    FOREIGN KEY (User_id) REFERENCES USER_ACCOUNTS(User_id) ON DELETE CASCADE
);
