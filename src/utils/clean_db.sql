/* 
   Smart Toll Booth System - Database Cleanup Script
   Drops all tables in the SmartTollSystem database.
*/

USE SmartTollSystem;
GO

-- Drop tables in reverse order of dependencies to avoid foreign key constraint errors
IF OBJECT_ID('dbo.Passage_Log', 'U') IS NOT NULL DROP TABLE dbo.Passage_Log;
IF OBJECT_ID('dbo.Cars', 'U') IS NOT NULL DROP TABLE dbo.Cars;
IF OBJECT_ID('dbo.Drivers', 'U') IS NOT NULL DROP TABLE dbo.Drivers;
GO
