-- ClearDB.sql file
-- clears the three relations

-- set use correctly
USE healthPortalDB;

-- disbale foreign key becuase it creates conflict
SET FOREIGN_KEY_CHECKS = 0;

-- drop entire db
-- DROP DATABASE healthPortalDB;

-- drop tables
DROP TABLE USER_ACCOUNTS;
DROP TABLE RECORDS;
DROP TABLE DOCTORS;
DROP TABLE APPOINTMENTS;
DROP TABLE BILLING;

-- enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;