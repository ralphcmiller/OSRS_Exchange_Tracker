# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import json

from datetime import datetime

def getPrice(itemIDs = []):
    headers = {
        'User-Agent': 'Tracking Price Fluctuations',
        'From': 'Ralph#8350'  # This is another valid field
    }
    
    response = requests.get('http://prices.runescape.wiki/api/v1/osrs/latest', headers=headers)
    data = response.json()

    nest = data['data']

    item_low = nest['564']['low']
    item_low_time = nest['564']['lowTime']
    item_hi = nest['564']['high']
    item_hi_time = nest['564']['highTime']

    print(item_low, datetime.fromtimestamp(item_low_time), item_hi, datetime.fromtimestamp(item_hi_time))    
    
    for x in itemIDs:
        print(x)

itemIDs = [554, 555]
getPrice(itemIDs)