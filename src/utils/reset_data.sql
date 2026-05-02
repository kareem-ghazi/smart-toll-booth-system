/* 
   Smart Toll Booth System - Data Reset Script
   Clears all data from the tables without dropping the schema.
   Uses DELETE instead of TRUNCATE to avoid foreign key constraint errors.
*/

USE SmartTollSystem;
GO

-- 1. Clear Passage_Log (Child table)
DELETE FROM Passage_Log;

-- 2. Clear Cars (Parent of Passage_Log, Child of Drivers)
DELETE FROM Cars;

-- 3. Clear Drivers (Parent of Cars)
DELETE FROM Drivers;

-- Optional: Reset Identity seed for Passage_Log
DBCC CHECKIDENT ('Passage_Log', RESEED, 0);

PRINT 'All data cleared successfully while respecting foreign key constraints.';
GO
