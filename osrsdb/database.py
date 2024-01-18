import sqlite3
from datetime import datetime

# Variables for database creation
items_table_sql = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT,
    last_updated TEXT,
    price_high INTEGER,
    price_low INTEGER,
    buy_limit INTEGER,
    high_five_min_vol INTEGER,
    low_five_min_vol INTEGER,
    avg_high_five_min_price INTEGER,
    avg_low_five_min_price INTEGER,
    high_hr_vol INTEGER,
    low_hr_vol INTEGER,
    avg_high_hr_price INTEGER,
    avg_low_hr_price INTEGER,
    lowalch INTEGER,
    highalch INTEGER,
    examine TEXT,
    wiki_url TEXT
);
"""
item_history_table_sql = """
CREATE TABLE IF NOT EXISTS item_history (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    price_high INTEGER,
    price_low INTEGER,
    high_five_min_vol INTEGER,
    low_five_min_vol INTEGER,
    avg_high_five_min_price INTEGER,
    avg_low_five_min_price INTEGER,
    high_hr_vol INTEGER,
    low_hr_vol INTEGER,
    avg_high_hr_price INTEGER,
    avg_low_hr_price INTEGER,
    timestamp TEXT,
    FOREIGN KEY (item_id) REFERENCES items (id)
);
"""

def create_connection():
    # Connects to the database and returns the connection object
    conn = None
    try:
        conn = sqlite3.connect("osrs_prices.db")
        print("Connection established to the database")
        # Create tables
        create_table(conn, items_table_sql)
        create_table(conn, item_history_table_sql)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def update_items_table(conn, item_data):
    """ Update or insert new records into the items table """
    sql = ''' INSERT OR REPLACE INTO items
              (id, name, last_updated, price_high, price_low, buy_limit,
               high_five_min_vol, low_five_min_vol, avg_high_five_min_price, 
               avg_low_five_min_price, high_hr_vol, low_hr_vol, avg_high_hr_price, 
               avg_low_hr_price, lowalch, highalch, examine, wiki_url) 
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cursor = conn.cursor()
    for item_id, data in item_data.items():
        # Parse the data to match the database columns
        item = (item_id, data.get('name'), datetime.now(), 
                data.get('price_high'), data.get('price_low'), data.get('buy_limit'),
                data.get('high_five_min_vol'), data.get('low_five_min_vol'), data.get('avg_high_five_min_price'), 
                data.get('avg_low_five_min_price'), data.get('high_hr_vol'), data.get('low_hr_vol'), data.get('avg_high_hr_price'), 
                data.get('avg_low_hr_price'), data.get('lowalch'), data.get('highalch'), data.get('examine'), data.get('wiki_url'))
        cursor.execute(sql, item)
    conn.commit()

def update_item_history_table(conn, item_history_data):
    """ Insert new records into the item_history table """
    sql = ''' INSERT INTO item_history
              (item_id, price_high, price_low, 
               high_five_min_vol, low_five_min_vol, avg_high_five_min_price, avg_low_five_min_price, 
               high_hr_vol, low_hr_vol, avg_high_hr_price, avg_low_hr_price, timestamp) 
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
    cursor = conn.cursor()
    for item_id, data in item_history_data.items():
        item_history = (item_id, 
                        data.get('price_high'), data.get('price_low'), 
                        data.get('high_five_min_vol'), data.get('low_five_min_vol'), 
                        data.get('avg_high_five_min_price'), data.get('avg_low_five_min_price'), 
                        data.get('high_hr_vol'), data.get('low_hr_vol'), 
                        data.get('avg_high_hr_price'), data.get('avg_low_hr_price'), 
                        datetime.now())
        cursor.execute(sql, item_history)
    conn.commit()
