from database import db_manager
import pandas as pd

def run_test():
    print("--- Starting Database Connection Test ---")
    
    # 1. Test Connection
    success, message = db_manager.test_connection()
    print(f"Connection Check: {message}")
    
    if not success:
        print("\n[TIP] Check if 'ODBC Driver 17 for SQL Server' is installed.")
        print("[TIP] Check if your SQL Server is running and the name is correct.")
        return

    # 2. Test Recording a Passage
    print("\nAttempting to record a test passage (Plate: TEST-999)...")
    rec_success, rec_msg = db_manager.record_passage("TEST-999", "Test-Vehicle", 10.50)
    print(f"Record Check: {rec_msg}")

    # 3. Test Fetching Data
    if rec_success:
        print("\nFetching recent logs from database:")
        df = db_manager.get_recent_logs(limit=5)
        if not df.empty:
            print(df)
        else:
            print("Database connected, but no logs were found.")

if __name__ == "__main__":
    run_test()
