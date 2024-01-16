import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('osrs_prices.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the 'items' table with the new columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        last_updated TEXT,
        members BOOLEAN,
        tradeable BOOLEAN,
        tradeable_on_ge BOOLEAN,
        stackable BOOLEAN,
        price_high INTEGER,
        price_low INTEGER,
        lowalch INTEGER,
        highalch INTEGER,
        buy_limit INTEGER,
        release_date TEXT,
        examine TEXT,
        icon TEXT,
        wiki_url TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create a new table to store historical data points
cursor.execute('''
    CREATE TABLE IF NOT EXISTS item_history (
        id INTEGER PRIMARY KEY,
        item_id INTEGER,
        price_high INTEGER,
        price_low INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_id) REFERENCES items(id)
    )
''')

# Commit changes and close the database connection
conn.commit()
conn.close()

print("SQLite database established.")
