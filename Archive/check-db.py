from osrsdb.process import process_and_store_api_data
from osrsdb.database import create_connection

def main():

    # Process and store API data
    print("Processing and storing API data...")
    process_and_store_api_data()

    print("Data processing and storage complete.")

    # Database connection
    conn = create_connection()

    log_file_path = "database_log.txt"

    with open(log_file_path, 'w') as log_file:
        # Querying the items table
        log_file.write("Items in the database:\n")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        for item in items:
            log_file.write(str(item) + '\n')

        # Querying the item_history table
        log_file.write("\nItem history in the database:\n")
        cursor.execute("SELECT * FROM item_history")
        history = cursor.fetchall()
        for record in history:
            log_file.write(str(record) + '\n')

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
