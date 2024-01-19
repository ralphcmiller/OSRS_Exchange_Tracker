import json
from datetime import datetime
from osrsdb.api import fetch_latest_prices, fetch_5m_prices, fetch_1h_prices
from osrsdb.database import create_connection, update_items_table, update_item_history_table
from osrsdb.itemmapping import load_item_mapping

def find_mapping_data(item_mapping, item_id):
    for item in item_mapping:
        if item['id'] == item_id:
            return item
    return {}  # Return an empty dictionary if no matching item is found

def process_and_store_api_data():
    item_mapping = load_item_mapping()

    conn = create_connection()

    # Fetch data from APIs
    latest_prices = fetch_latest_prices()
    prices_5m = fetch_5m_prices()
    prices_1h = fetch_1h_prices()

    items_data = {}
    item_history_data = {}
    for item_id_str, latest_data in latest_prices.items():
        item_id = int(item_id_str)  # Convert string ID to integer
        mapping_data = find_mapping_data(item_mapping, item_id)
        data_5m = prices_5m.get(str(item_id), {})
        data_1h = prices_1h.get(str(item_id), {})

        # Get item name; if None, set a default value like an empty string
        item_name = mapping_data.get('name', '')
        # Construct the wiki URL
        wiki_url = "https://oldschool.runescape.wiki/w/" + item_name.replace(' ', '_') if item_name else ''
        #Calculate margin
        high_value = latest_data.get('high')
        low_value = latest_data.get('low')
        # Check if 'high' and 'low' are not None and are integers
        if high_value is not None and low_value is not None and isinstance(high_value, int) and isinstance(low_value, int):
            margin = high_value - low_value
        else:
            # Set margin to None if 'high' or 'low' is missing or not an integer
            margin = None 

        items_data[item_id] = {
            'id': item_id,
            'name': mapping_data.get('name'),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'price_high': latest_data.get('high'),
            'price_low': latest_data.get('low'),
            'buy_limit': mapping_data.get('limit'),
            'high_five_min_vol': data_5m.get('highPriceVolume'),
            'low_five_min_vol': data_5m.get('lowPriceVolume'),
            'avg_high_five_min_price': data_5m.get('avgHighPrice'),
            'avg_low_five_min_price': data_5m.get('avgLowPrice'),
            'high_hr_vol': data_1h.get('highPriceVolume'),
            'low_hr_vol': data_1h.get('lowPriceVolume'),
            'avg_high_hr_price': data_1h.get('avgHighPrice'),
            'avg_low_hr_price': data_1h.get('avgLowPrice'),
            'lowalch': mapping_data.get('lowalch'),
            'highalch': mapping_data.get('highalch'),
            'examine': mapping_data.get('examine'),
            'wiki_url': wiki_url,
            'margin': margin,
        }

        # Data for item_history table
        item_history_data[item_id] = {
            'item_id': item_id,
            'price_high': latest_data.get('high'),
            'price_low': latest_data.get('low'),
            'high_five_min_vol': data_5m.get('highPriceVolume'),
            'low_five_min_vol': data_5m.get('lowPriceVolume'),
            'avg_high_five_min_price': data_5m.get('avgHighPrice'),
            'avg_low_five_min_price': data_5m.get('avgLowPrice'),
            'high_hr_vol': data_1h.get('highPriceVolume'),
            'low_hr_vol': data_1h.get('lowPriceVolume'),
            'avg_high_hr_price': data_1h.get('avgHighPrice'),
            'avg_low_hr_price': data_1h.get('avgLowPrice'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    # Store in database
    update_items_table(conn, items_data)
    update_item_history_table(conn, item_history_data)

    conn.close()

