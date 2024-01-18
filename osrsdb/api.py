import requests

BASE_URL = "https://prices.runescape.wiki/api/v1/osrs"

def fetch_api_data(endpoint):
    """Fetch data from a given API endpoint."""
    url = f"{BASE_URL}/{endpoint}"
    headers = {'User-Agent': 'Tracking Price Fluctuations', 'From': 'Discord: @ralph_3'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        
        # Check if 'data' key exists in the response
        if 'data' in json_response:
            return json_response['data']
        else:
            return json_response
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def fetch_latest_prices():
    return fetch_api_data("latest")

def fetch_5m_prices():
    return fetch_api_data("5m")

def fetch_1h_prices():
    return fetch_api_data("1h")

def fetch_item_mapping():
    return fetch_api_data("mapping")

