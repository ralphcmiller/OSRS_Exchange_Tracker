import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('osrs_prices.db')
cursor = conn.cursor()

# Function to check if there is data in the 'items' table
def check_data_in_items_table():
    try:
        # Execute a SELECT query to count the rows in the 'items' table
        cursor.execute("SELECT COUNT(*) FROM items;")
        row_count = cursor.fetchone()[0]

        if row_count > 0:
            print("There is data in the 'items' table.")
        else:
            print("The 'items' table is empty.")

    except sqlite3.Error as e:
        print("Error:", e)

# Call the function to check for data in the 'items' table
check_data_in_items_table()

# Close the database connection
conn.close()
