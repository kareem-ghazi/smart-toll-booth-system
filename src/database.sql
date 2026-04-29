/* 
   Smart Toll System - Relational Database Schema
   Tables: Cars, Passage_Log, Drivers
*/

-- 0. Create Database
CREATE DATABASE SmartTollSystem;
GO
USE SmartTollSystem;
GO

-- 1. Drivers Table
CREATE TABLE Drivers (
    NID VARCHAR(20) PRIMARY KEY,
    Full_Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    Address TEXT,
    License_Expiry DATE
);

-- 2. Cars Table
CREATE TABLE Cars (
    License_Plate NVARCHAR(20) PRIMARY KEY,
    Car_Type VARCHAR(50) NOT NULL,
    Brand VARCHAR(50),
    Model VARCHAR(50),
    Manufacture_Year INT,
    Owed_Fees DECIMAL(10, 2) DEFAULT 0.00,
    Owner_NID VARCHAR(20) NOT NULL,
    Last_Seen DATETIME,
    CONSTRAINT FK_Cars_Drivers FOREIGN KEY (Owner_NID) REFERENCES Drivers(NID)
);

-- 3. Passage_Log Table
CREATE TABLE Passage_Log (
    Log_ID INT IDENTITY(1,1) PRIMARY KEY,
    License_Plate NVARCHAR(20) NOT NULL,
    Applied_Fee DECIMAL(10, 2) NOT NULL,
    Passing_Time DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Log_Cars FOREIGN KEY (License_Plate) REFERENCES Cars(License_Plate)
);
GO

-- =============================================
-- Data Population
-- =============================================

-- Drivers (25)
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('283012446048', N'Ahmed Mohamed', '01012345678', N'Cairo', '2027-04-05');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('283112481482', N'Mahmoud Ali', '01123456789', N'Alexandria', '2026-10-14');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('281010338657', N'Sara Hassan', '01234567890', N'Giza', '2027-09-20');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('280090795181', N'Layla Youssef', '01545678901', N'Mansoura', '2031-09-14');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('287081946463', N'Omar Khaled', '01098765432', N'Tanta', '2032-01-25');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('285121454597', N'Mariam Ibrahim', '01187654321', N'Suez', '2028-03-07');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('290020359797', N'Yassin Tarek', '01276543210', N'Port Said', '2026-06-28');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('291100915695', N'Nour El-Din', '01565432109', N'Ismailia', '2031-08-18');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('283070382357', N'Fatima El-Zahraa', '01011223344', N'Luxor', '2028-11-20');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('291100719116', N'Mostafa Mahmoud', '01122334455', N'Aswan', '2026-11-08');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('289022840512', N'Zainab Sayed', '01233445566', N'Assiut', '2032-02-13');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('288082157819', N'Hany Ramzy', '01544556677', N'Sohag', '2027-06-12');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('286110999593', N'Mona Zaki', '01055667788', N'Qena', '2031-02-20');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('285092442087', N'Karim Abdel Aziz', '01166778899', N'Minya', '2027-08-13');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('288112383000', N'Hend Sabry', '01277889900', N'Beni Suef', '2027-11-11');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('281042714207', N'Tamer Hosny', '01011112222', N'Fayoum', '2032-06-13');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('288020784341', N'Amr Diab', '01122223333', N'Damietta', '2031-06-07');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('295072170142', N'Sherine Abdel Wahab', '01233334444', N'Beheira', '2027-05-05');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('287121880644', N'Mohamed Salah', '01544445555', N'Sharqia', '2028-12-19');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('293101357447', N'Essam El-Hadary', '01055556666', N'Gharbia', '2027-03-17');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('295022516175', N'Adel Emam', '01166667777', N'Monufia', '2032-02-05');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('285111488172', N'Yousra', '01277778888', N'Qalyubia', '2026-07-13');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('299081742953', N'Ahmed Helmy', '01588889999', N'Kafr El Sheikh', '2030-01-22');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('283111844973', N'Mona El-Shazly', '01099990000', N'Matrouh', '2032-11-11');
INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('283051430730', N'Bassem Youssef', '01100001111', N'Red Sea', '2029-01-24');

-- Cars (50 from experimental/)
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ج ب ط - ٣٩٤٥', 'Pickup', 'Renault', 'Logan', 2013, '295022516175');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ن ط و - ١', 'Pickup', 'Renault', 'Megane', 2016, '287081946463');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ق ق ن - ٧٤٨', 'Pickup', 'Kia', 'Picanto', 2010, '293101357447');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ى و ر - ٤٨٥١', 'Pickup', 'Chevrolet', 'Optra', 2013, '288082157819');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'د ق ص - ٢٤١١', 'Pickup', 'Nissan', 'Sunny', 2017, '287121880644');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ط د - ١', 'Sedan', 'Hyundai', 'Tucson', 2025, '281010338657');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ى و ق - ١١١١', 'Hatchback', 'Kia', 'Sportage', 2025, '295072170142');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'م م - ٦٦٦٦', 'SUV', 'Mitsubishi', 'Eclipse', 2023, '290020359797');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'س ع - ١', 'Hatchback', 'Nissan', 'Sentra', 2019, '286110999593');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ى د ھ - ١١١١', 'Pickup', 'Chevrolet', 'Cruze', 2024, '280090795181');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ى ل ع - ٨٨٨', 'SUV', 'Nissan', 'Sunny', 2020, '283012446048');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ع ھ ق - ٥٨٤٧', 'Hatchback', 'Renault', 'Logan', 2017, '283012446048');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ى ل ع - ١', 'Sedan', 'Toyota', 'Corolla', 2012, '283112481482');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ر ص م - ٢', 'Pickup', 'Hyundai', 'Tucson', 2017, '283070382357');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'د س أ - ٤١٤', 'Van', 'Nissan', 'Sentra', 2014, '283111844973');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ر د ب - ٨٨٨٨', 'Hatchback', 'Fiat', '500', 2017, '281042714207');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'م - ٣', 'Van', 'Nissan', 'Sunny', 2013, '285111488172');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'أ أ - ١١', 'Van', 'BMW', '520i', 2023, '288112383000');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ل ف د - ٦٦٦', 'Sedan', 'Hyundai', 'Elantra', 2022, '283111844973');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ر أ س - ٥٥٥', 'Pickup', 'Hyundai', 'Elantra', 2016, '290020359797');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ى ل ع - ٩٩٩٩', 'Hatchback', 'Chevrolet', 'Optra', 2023, '285121454597');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ب ج ر - ٦٦٦', 'Pickup', 'Chevrolet', 'Optra', 2012, '288112383000');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ع م - ٦٦٦٦', 'Hatchback', 'Hyundai', 'Elantra', 2010, '281010338657');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ع ل د - ٦٦٦٦', 'SUV', 'Kia', 'Cerato', 2025, '281042714207');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ج ج ج - ٥٥٥', 'SUV', 'Mercedes', 'C200', 2015, '286110999593');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'أ أ س - ١١١١', 'Sedan', 'Mercedes', 'E200', 2024, '291100719116');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'و - ١١', 'Van', 'Renault', 'Megane', 2025, '287081946463');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ھ ھ - ٢٢', 'SUV', 'Mitsubishi', 'Lancer', 2011, '287121880644');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ى ل ع - ٣٣٣', 'Hatchback', 'Toyota', 'Fortuner', 2020, '283112481482');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ع ع ع - ٢٢٢٢', 'Sedan', 'Fiat', '500', 2015, '283112481482');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'د ى س - ٧٧٧', 'Hatchback', 'Hyundai', 'Elantra', 2012, '293101357447');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ر م ن - ٧٧', 'Sedan', 'Nissan', 'Qashqai', 2013, '287121880644');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'أ أ - ١', 'SUV', 'Fiat', 'Punto', 2011, '293101357447');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'و - ١١', 'Sedan', 'Mercedes', 'GLC', 2020, '283070382357');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ف ف - ١١١١', 'SUV', 'BMW', '320i', 2018, '286110999593');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'أ أ - ١', 'SUV', 'Mitsubishi', 'Pajero', 2020, '283051430730');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ص ص - ٢٢٢٢', 'Sedan', 'Toyota', 'Yaris', 2013, '281010338657');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ف ف ف - ٥٥٥٥', 'Hatchback', 'Nissan', 'Sentra', 2018, '287081946463');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'و - ١', 'Pickup', 'Hyundai', 'Elantra', 2021, '291100719116');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ھ - ١', 'SUV', 'Chevrolet', 'Cruze', 2019, '293101357447');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ف ى س - ١', 'Hatchback', 'Toyota', 'Fortuner', 2019, '285111488172');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ف ف ف - ٥٥٥٥', 'Sedan', 'Kia', 'Cerato', 2013, '280090795181');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'م م م - ١', 'Hatchback', 'Kia', 'Cerato', 2019, '293101357447');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'د س أ - ١', 'SUV', 'BMW', '320i', 2018, '288020784341');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'د - ١', 'Van', 'Mitsubishi', 'Lancer', 2012, '295022516175');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ر - ١', 'Van', 'Mitsubishi', 'Lancer', 2010, '289022840512');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'ل ل ل - ١١١١', 'SUV', 'Mitsubishi', 'Lancer', 2024, '295072170142');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'د ى س - ٣٣٣٣', 'Van', 'Renault', 'Logan', 2013, '281010338657');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'و - ١١', 'SUV', 'Renault', 'Logan', 2021, '287121880644');
INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'و - ١١', 'Hatchback', 'Kia', 'Cerato', 2014, '283112481482');
