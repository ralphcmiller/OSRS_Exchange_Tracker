import sqlite3
from datetime import datetime, timedelta

def clean_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('osrs_prices.db')
    cursor = conn.cursor()

    # Calculate the timestamp cutoff (24 hours ago from the current time)
    cutoff_time = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')

    # Delete records older than the cutoff time from the item_history table
    cursor.execute("DELETE FROM item_history WHERE timestamp < ?", (cutoff_time,))
    conn.commit()

    # Get the number of records deleted
    deleted_records = cursor.rowcount

    # Close the database connection
    conn.close()
    if deleted_records > 0:
        print(f"{deleted_records} old records deleted from the item_history database.")
    else:
        print("No old records found to delete.")

    return
