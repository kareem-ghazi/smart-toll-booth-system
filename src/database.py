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
            
            # Update car's owed fees and last seen time if it exists
            update_car_query = """
            UPDATE Cars 
            SET Owed_Fees = Owed_Fees + ?, 
                Last_Seen = GETDATE(),
                Car_Type = ?
            WHERE License_Plate = ?;
            """
            cursor.execute(update_car_query, (fee, car_type, plate))

            # Record in passage log
            # Note: This will only succeed if the car exists in Cars table due to FK constraint
            log_query = """
            INSERT INTO Passage_Log (License_Plate, Applied_Fee, Passing_Time)
            VALUES (?, ?, GETDATE());
            """
            cursor.execute(log_query, (plate, fee))

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
        except Exception as e:
            print(f"DEBUG: Error fetching dataframe -> {e}")
            return pd.DataFrame()
        finally:
            conn.close()

    def get_recent_logs(self, limit=100):
        query = f"SELECT TOP {limit} License_Plate, Applied_Fee, Passing_Time FROM Passage_Log ORDER BY Passing_Time DESC"
        return self._fetch_as_dataframe(query)

    def get_all_cars(self):
        query = "SELECT * FROM Cars ORDER BY Last_Seen DESC"
        return self._fetch_as_dataframe(query)

    def get_all_drivers(self):
        query = "SELECT * FROM Drivers"
        return self._fetch_as_dataframe(query)

db_manager = DatabaseManager()
