import json
from osrsdb.api import fetch_item_mapping

import json
from osrsdb.api import fetch_item_mapping

def download_and_save_item_mapping():
    item_mapping_data = fetch_item_mapping()
    if item_mapping_data is not None:
        # Save the full item mapping
        with open('item_mapping.json', 'w') as file:
            json.dump(item_mapping_data, file)
        print("Item mapping saved to item_mapping.json")

        # Extract and save item names
        item_names = [item['name'] for item in item_mapping_data]
        with open('static/item_names.json', 'w') as file:
            json.dump(item_names, file)
        print("Item names saved to static/item_names.json")
    else:
        print("Failed to fetch item mapping data")


def load_item_mapping():
    try:
        with open('item_mapping.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("item_mapping.json not found. Downloading now.")
        download_and_save_item_mapping()
        with open('item_mapping.json', 'r') as file:
            return json.load(file)
