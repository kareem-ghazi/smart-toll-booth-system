import pyodbc
import pandas as pd
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        # --- CONFIGURATION ---
        self.server = 'DESKTOP-AV54BGA\\SQLEXPRESS' 
        self.database = 'SmartTollSystem'
        self.username = 'YOUR_USERNAME'
        self.password = 'YOUR_PASSWORD'
        
        self.conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'Trusted_Connection=yes;'
        )

    def _get_connection(self):
        try:
            conn = pyodbc.connect(self.conn_str, timeout=5)
            conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-16le')
            conn.setencoding(encoding='utf-16le')
            return conn
        except Exception as e:
            print(f"DEBUG: Connection Error -> {e}")
            raise

    def test_connection(self):
        try:
            conn = self._get_connection()
            conn.close()
            return True, "Successfully connected to SQL Server!"
        except Exception as e:
            return False, f"Failed to connect: {str(e)}"

    def record_passage(self, plate, car_type, fee):
        """Records a car passage with transaction safety and debugging."""
        conn = None
        try:
            print(f"DEBUG: Attempting to record passage for plate: {plate}")
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Simplified MERGE to avoid issues with missing columns like 'last_seen'
            upsert_query = """
            MERGE INTO Cars AS target
            USING (SELECT ? AS plate, ? AS car_type, ? AS fee) AS source
            ON target.plate = source.plate
            WHEN MATCHED THEN
                UPDATE SET 
                    pass_count = target.pass_count + 1,
                    total_fees = target.total_fees + source.fee,
                    car_type = source.car_type
            WHEN NOT MATCHED THEN
                INSERT (plate, car_type, pass_count, total_fees)
                VALUES (source.plate, source.car_type, 1, source.fee);
            """
            cursor.execute(upsert_query, (plate, car_type, fee))

            log_query = """
            INSERT INTO Log (plate, fee, car_type, time)
            VALUES (?, ?, ?, GETDATE());
            """
            cursor.execute(log_query, (plate, fee, car_type))

            conn.commit()
            print(f"DEBUG: Successfully recorded {plate}")
            return True, "Success"
        except Exception as e:
            print(f"DEBUG: ERROR in record_passage -> {e}")
            if conn: conn.rollback()
            return False, str(e)
        finally:
            if conn: conn.close()

    def _fetch_as_dataframe(self, query):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            data = [list(row) for row in rows]
            return pd.DataFrame(data, columns=columns)
        finally:
            conn.close()

    def get_recent_logs(self, limit=100):
        query = f"SELECT TOP {limit} plate, car_type, fee, time FROM Log ORDER BY time DESC"
        return self._fetch_as_dataframe(query)

    def get_all_cars(self):
        # Removed 'last_seen' from query to fix the crash
        query = "SELECT plate, car_type, pass_count, total_fees FROM Cars ORDER BY pass_count DESC"
        return self._fetch_as_dataframe(query)

    def get_all_drivers(self):
        query = "SELECT nid, name, phone, plate, last_update FROM Drivers"
        return self._fetch_as_dataframe(query)

db_manager = DatabaseManager()
