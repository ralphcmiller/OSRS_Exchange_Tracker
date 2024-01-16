from flask import Flask, render_template, jsonify
import sqlite3
import json
import threading
import subprocess
import time

app = Flask(__name__)

# Your existing route for displaying items
@app.route('/')
def display_items():
    # Connect to the SQLite database
    conn = sqlite3.connect('osrs_prices.db')
    cursor = conn.cursor()

    # Fetch item data from the 'items' table
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()

    # Fetch item names from decorated_items.json (or your new JSON file)
    with open('json/item_names.json', 'r') as json_file:
        item_names = json.load(json_file)

    # Close the database connection
    conn.close()

    # Render an HTML template and pass the item data and item_names to it
    return render_template('items.html', items=items, item_names=item_names)

# New route for fetching historical data
@app.route('/historical_data/<int:item_id>')
def get_historical_data(item_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('osrs_prices.db')
    cursor = conn.cursor()

    # Fetch historical data for the specified item from the 'item_history' table
    cursor.execute("SELECT timestamp, price_high, price_low FROM item_history WHERE item_id = ? ORDER BY timestamp", (item_id,))
    historical_data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert historical data to a list of dictionaries
    data = [{'timestamp': row[0], 'price_high': row[1], 'price_low': row[2]} for row in historical_data]
    # Return historical data as JSON response
    return jsonify(data)

def run_fetch_prices_script():
    while True:
        # Run the fetch-prices.py script using subprocess
        try:
            subprocess.run(['python', 'functions/fetch-prices.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running fetch-prices.py: {e}")
        # Sleep for a specified interval (in seconds)
        time.sleep(300)  # 5min interval

# New route for manually triggering data update
@app.route('/fetch_updated_data', methods=['POST'])
def fetch_updated_data():
    # Run the fetch-prices.py script using subprocess
    try:
        subprocess.run(['python', 'functions/fetch-prices.py'], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'message': f"Error running fetch-prices.py: {e}"}), 500
    
    return jsonify({'message': 'Data update successful'}), 200

# Function to run the cleanup-db.py script
def run_cleanup_db_script():
    while True:
        # Run the cleanup-db.py script using subprocess
        try:
            subprocess.run(['python', 'functions/cleanup-db.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running cleanup-db.py: {e}")
        # Sleep for a specified interval (in seconds)
        time.sleep(3600)  # 1 hour interval

if __name__ == '__main__':
    # Create a thread to run the fetch-prices.py script
    fetch_prices_thread = threading.Thread(target=run_fetch_prices_script)
    fetch_prices_thread.daemon = True
    fetch_prices_thread.start()

    # Create a thread to run the cleanup-db.py script
    cleanup_db_thread = threading.Thread(target=run_cleanup_db_script)
    cleanup_db_thread.daemon = True
    cleanup_db_thread.start()

    # Start the Flask app
    app.run(debug=True)