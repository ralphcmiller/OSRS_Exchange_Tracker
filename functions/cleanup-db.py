import sqlite3
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('osrs_prices.db')
cursor = conn.cursor()

# Calculate the timestamp cutoff (24 hours ago from the current time)
cutoff_time = datetime.now() - timedelta(hours=24)

# Delete records older than the cutoff time
cursor.execute("DELETE FROM items WHERE timestamp < ?", (cutoff_time,))
conn.commit()

# Get the number of records deleted
deleted_records = cursor.rowcount

# Close the database connection
conn.close()

if deleted_records > 0:
    print(f"{deleted_records} old records deleted from the database.")
else:
    print("No old records found to delete.")
