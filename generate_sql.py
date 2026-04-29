import random

# Character mapping from src/data/processed_plates/data.yaml
chars = [
    "أ", "ب", "ج", "د", "ر", "س", "ص", "ط", "ع", "ف", "ق", "ل", "م", "ن", "ھ", "و", "ى",
    "٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"
]

# This data was previously extracted using extract_plates.py
plates_raw = [
    ("0002.jpg", "٣٩٤٥جبط"), ("0003.jpg", "١نطو"), ("0010.jpg", "٧٤٨ققن"), ("0015.jpg", "٤٨٥١ىور"),
    ("0028.jpg", "٢٤١١دقص"), ("0034.jpg", "١طد"), ("0041.jpg", "١١١١ىوق"), ("0044.jpg", "٦٦٦٦مم"),
    ("0047.jpg", "١سع"), ("0052.jpg", "١١١١ىدھ"), ("0054.jpg", "٨٨٨ىلع"), ("0055.jpg", "٥٨٤٧عھق"),
    ("0065.jpg", "١ىلع"), ("0072.jpg", "٢رصم"), ("0082.jpg", "٤١٤دسأ"), ("0082.jpg", "٤١٤دسأ"),
    ("0084.jpg", "٨٨٨٨ردب"), ("0096.jpg", "٣م"), ("0108.jpg", "١١أأ"), ("0114.jpg", "٦٦٦لفد"),
    ("0115.jpg", "٥٥٥رأس"), ("0118.jpg", "٩٩٩٩ىلع"), ("0120.jpg", "٦٦٦بجر"), ("0123.jpg", "٦٦٦٦عم"),
    ("0124.jpg", "٦٦٦٦علد"), ("0125.jpg", "٥٥٥ججج"), ("0126.jpg", "١١١١أأس"), ("0128.jpg", "١١و"),
    ("0138.jpg", "٢٢ھھ"), ("0145.jpg", "٣٣٣ىلع"), ("0148.jpg", "٢٢٢٢ععع"), ("0160.jpg", "٧٧٧دىس"),
    ("0162.jpg", "٧٧رمن"), ("0163.jpg", "١أأ"), ("0170.jpg", "١١و"), ("0175.jpg", "١١١١فف"),
    ("0177.jpg", "١أأ"), ("0185.jpg", "٢٢٢٢صص"), ("0188.jpg", "٥٥٥٥ففف"), ("0190.jpg", "١و"),
    ("0192.jpg", "١ھ"), ("0195.jpg", "١فىس"), ("0196.jpg", "٥٥٥٥ففف"), ("0198.jpg", "١ممم"),
    ("0202.jpg", "١دسأ"), ("0205.jpg", "١د"), ("0208.jpg", "١ر"), ("0211.jpg", "١١١١للل"),
    ("0218.jpg", "٣٣٣٣دىس"), ("0222.jpg", "١١و"), ("0223.jpg", "١١و")
]

# Formatting plates to look more like 'أ ب ج - ١٢٣'
def format_plate(p):
    digits = "".join([c for c in p if c in "٠١٢٣٤٥٦٧٨٩"])
    letters = "".join([c for c in p if c not in "٠١٢٣٤٥٦٧٨٩"])
    return f"{' '.join(letters)} - {digits}"

plates = [(f, format_plate(p)) for f, p in plates_raw]

brands = ["Toyota", "Hyundai", "Kia", "Nissan", "Mitsubishi", "BMW", "Mercedes", "Chevrolet", "Renault", "Fiat"]
models = {
    "Toyota": ["Corolla", "Yaris", "Fortuner"],
    "Hyundai": ["Elantra", "Accent", "Tucson"],
    "Kia": ["Sportage", "Cerato", "Picanto"],
    "Nissan": ["Sunny", "Qashqai", "Sentra"],
    "Mitsubishi": ["Lancer", "Pajero", "Eclipse"],
    "BMW": ["320i", "520i", "X5"],
    "Mercedes": ["C200", "E200", "GLC"],
    "Chevrolet": ["Optra", "Aveo", "Cruze"],
    "Renault": ["Logan", "Duster", "Megane"],
    "Fiat": ["Tipo", "500", "Punto"]
}
types = ["Sedan", "SUV", "Pickup", "Van", "Hatchback"]

drivers_data = [
    ("Ahmed Mohamed", "01012345678", "Cairo"),
    ("Mahmoud Ali", "01123456789", "Alexandria"),
    ("Sara Hassan", "01234567890", "Giza"),
    ("Layla Youssef", "01545678901", "Mansoura"),
    ("Omar Khaled", "01098765432", "Tanta"),
    ("Mariam Ibrahim", "01187654321", "Suez"),
    ("Yassin Tarek", "01276543210", "Port Said"),
    ("Nour El-Din", "01565432109", "Ismailia"),
    ("Fatima El-Zahraa", "01011223344", "Luxor"),
    ("Mostafa Mahmoud", "01122334455", "Aswan"),
    ("Zainab Sayed", "01233445566", "Assiut"),
    ("Hany Ramzy", "01544556677", "Sohag"),
    ("Mona Zaki", "01055667788", "Qena"),
    ("Karim Abdel Aziz", "01166778899", "Minya"),
    ("Hend Sabry", "01277889900", "Beni Suef"),
    ("Tamer Hosny", "01011112222", "Fayoum"),
    ("Amr Diab", "01122223333", "Damietta"),
    ("Sherine Abdel Wahab", "01233334444", "Beheira"),
    ("Mohamed Salah", "01544445555", "Sharqia"),
    ("Essam El-Hadary", "01055556666", "Gharbia"),
    ("Adel Emam", "01166667777", "Monufia"),
    ("Yousra", "01277778888", "Qalyubia"),
    ("Ahmed Helmy", "01588889999", "Kafr El Sheikh"),
    ("Mona El-Shazly", "01099990000", "Matrouh"),
    ("Bassem Youssef", "01100001111", "Red Sea")
]

random.seed(42)

sql = """/* 
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
"""

driver_nids = []
for i, (name, phone, address) in enumerate(drivers_data):
    nid = f"2{random.randint(80, 99)}{random.randint(1, 12):02d}{random.randint(1, 28):02d}{random.randint(10000, 99999)}"
    driver_nids.append(nid)
    expiry = f"20{random.randint(26, 32)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    sql += f"INSERT INTO Drivers (NID, Full_Name, Phone, Address, License_Expiry) VALUES ('{nid}', N'{name}', '{phone}', N'{address}', '{expiry}');\\n"

sql += "\\n-- Cars (50 from experimental/)\\n"

for f, plate in plates:
    car_type = random.choice(types)
    brand = random.choice(brands)
    model = random.choice(models[brand])
    year = random.randint(2010, 2025)
    owner_nid = random.choice(driver_nids)
    sql += f"INSERT INTO Cars (License_Plate, Car_Type, Brand, Model, Manufacture_Year, Owner_NID) VALUES (N'{plate}', '{car_type}', '{brand}', '{model}', {year}, '{owner_nid}');\\n"

with open("src/database.sql", "w", encoding="utf-8") as f:
    f.write(sql)
