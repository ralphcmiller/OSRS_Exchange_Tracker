import sqlite3
import requests
import json
from datetime import datetime

# Function to fetch latest price data from the RuneScape API
def fetch_latest_prices():
    url = "http://prices.runescape.wiki/api/v1/osrs/latest"
    headers = {
        'User-Agent': 'Tracking Price Fluctuations',
        'From': 'Ralph#8350'  # This is another valid field
    }
    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = json.loads(response.text)['data']

        # Print the fetched data for debugging
        #print("Fetched data:")
        #print(data)

        return data
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    return None

# Function to update the database with the latest price data
def update_database():
    latest_prices = fetch_latest_prices()
    if latest_prices is not None:
        # Read decorated items from JSON file
        with open('json/decorated_items.json', 'r') as f:
            decorated_items = json.load(f)

        conn = sqlite3.connect('osrs_prices.db')
        cursor = conn.cursor()

        # Update or insert records in the 'items' table with new price data and decoration
        for item_id, price_info in latest_prices.items():
            # Get decoration data from decorated_items.json
            decoration_data = decorated_items.get(item_id, {})
            
            cursor.execute(
                "INSERT OR REPLACE INTO items (id, name, last_updated, members, tradeable, "
                "tradeable_on_ge, stackable, price_high, price_low, lowalch, highalch, buy_limit, "
                "release_date, examine, icon, wiki_url, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (item_id, decoration_data.get('name', None), str(datetime.now()), 
                 decoration_data.get('members', None), decoration_data.get('tradeable', None),
                 decoration_data.get('tradeable_on_ge', None), decoration_data.get('stackable', None),
                 price_info.get('high', None), price_info.get('low', None), 
                 decoration_data.get('lowalch', None), decoration_data.get('highalch', None),
                 decoration_data.get('buy_limit', None), decoration_data.get('release_date', None),
                 decoration_data.get('examine', None), decoration_data.get('icon', None),
                 decoration_data.get('wiki_url', None), str(datetime.now()))
            )

            # Insert the data into the 'item_history' table
            cursor.execute(
                "INSERT INTO item_history (item_id, price_high, price_low) VALUES (?, ?, ?)",
                (item_id, price_info.get('high', None), price_info.get('low', None))
            )

        conn.commit()
        conn.close()

        print("Database updated with latest price data.")
    else:
        print("Failed to fetch latest price data.")

# Schedule this script to run periodically (e.g., hourly) to update the database
update_database()
