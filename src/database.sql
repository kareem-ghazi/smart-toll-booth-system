/* 
   Smart Toll System - Relational Database Schema
   Tables: Cars, Log, Drivers
*/

-- 0. Create Database
-- CREATE DATABASE SmartTollSystem
-- USE SmartTollSystem

-- 1. Cars Table (Central Relation)
CREATE TABLE Cars (
    plate NVARCHAR(20) PRIMARY KEY,        -- Using plate as the primary key for direct linkage
    car_type NVARCHAR(50),
    pass_count INT DEFAULT 0,
    total_fees DECIMAL(18, 2) DEFAULT 0.00,
    last_seen DATETIME DEFAULT GETDATE()
);

-- 2. Drivers Table (Personal Info)
CREATE TABLE Drivers (
    nid BIGINT PRIMARY KEY,                -- 14-digit National ID
    name NVARCHAR(100) NOT NULL,           -- Arabic Name
    phone NVARCHAR(11) NOT NULL,           -- 11-digit Phone
    last_update DATETIME DEFAULT GETDATE(),
    plate NVARCHAR(20) NOT NULL,
    CONSTRAINT FK_Drivers_Cars FOREIGN KEY (plate) REFERENCES Cars(plate)
);

-- 3. Log Table (Transaction History)
CREATE TABLE Log (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    plate NVARCHAR(20) NOT NULL,
    fee DECIMAL(18, 2) NOT NULL,
    time DATETIME DEFAULT GETDATE(),
    car_type NVARCHAR(50),
    CONSTRAINT FK_Log_Cars FOREIGN KEY (plate) REFERENCES Cars(plate)
);
GO

-- =============================================
-- Fake Data Generation (15 Drivers)
-- =============================================
-- Note: We insert into Cars first to satisfy Foreign Key constraints
INSERT INTO Cars (plate, car_type) VALUES 
(N'أ ب ج - ١٢٣', N'Sedan'), (N'س ص ع - ٤٥٦', N'SUV'), (N'ر ط ي - ٧٨٩', N'Pickup'),
(N'د ذ ر - ١١١', N'Van'), (N'ل م ن - ٢٢٢', N'Sport'), (N'ق ك ل - ٣٣٣', N'Hatchback'),
(N'و هـ ي - ٤٤٤', N'Off-road'), (N'ب ت ث - ٥٥٥', N'Sedan'), (N'ج ح خ - ٦٦٦', N'SUV'),
(N'س ش ص - ٧٧٧', N'Pickup'), (N'ط ظ ع - ٨٨٨', N'Van'), (N'ف ق ك - ٩٩٩', N'Sport'),
(N'م ن هـ - ٠٠٠', N'Hatchback'), (N'أ ب ت - ١٥٩', N'Off-road'), (N'ج د هـ - ٧٥٣', N'Sedan');

INSERT INTO Drivers (nid, name, phone, plate) VALUES 
(29501011234567, N'أحمد محمد', N'01012345678', N'أ ب ج - ١٢٣'),
(28805129876543, N'محمود علي', N'01123456789', N'س ص ع - ٤٥٦'),
(29208201122334, N'سارة حسن', N'01234567890', N'ر ط ي - ٧٨٩'),
(29903154455667, N'ليلى يوسف', N'01545678901', N'د ذ ر - ١١١'),
(28511307788990, N'عمر خالد', N'01098765432', N'ل م ن - ٢٢٢'),
(29104052233445, N'مريم إبراهيم', N'01187654321', N'ق ك ل - ٣٣٣'),
(29709215566778, N'ياسين طارق', N'01276543210', N'و هـ ي - ٤٤٤'),
(28302148899001, N'نور الدين', N'01565432109', N'ب ت ث - ٥٥٥'),
(29406183344556, N'فاطمة الزهراء', N'01011223344', N'ج ح خ - ٦٦٦'),
(28910056677889, N'مصطفى محمود', N'01122334455', N'س ش ص - ٧٧٧'),
(29607129900112, N'زينب سيد', N'01233445566', N'ط ظ ع - ٨٨٨'),
(28701252233441, N'هاني رمزي', N'01544556677', N'ف ق ك - ٩٩٩'),
(29312085566772, N'منى زكي', N'01055667788', N'م ن هـ - ٠٠٠'),
(28408198899003, N'كريم عبد العزيز', N'01166778899', N'أ ب ت - ١٥٩'),
(29804251122334, N'هند صبري', N'01277889900', N'ج د هـ - ٧٥٣');
