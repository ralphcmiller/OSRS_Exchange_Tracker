# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import json
import sql_database

from datetime import datetime

def getPrice():
    headers = {
        'User-Agent': 'Tracking Price Fluctuations',
        'From': 'Ralph#8350'  # This is another valid field
    }    
    response = requests.get('http://prices.runescape.wiki/api/v1/osrs/latest', headers=headers)
    data = response.json()
    nest = data['data']
    return nest

def getItemInfo(itemID):
    f = open('items.json')
    refrenceIDs = json.load(f)
    
    for i in refrenceIDs:
        if i == itemID:
            return refrenceIDs[i]
            
                
def createTable(setup, itemID):
    info = getItemInfo(itemID)
    if info is None:
        return -1
    table = info['name']
    print(table)
    if setup is True:
        sql_database.create_table(table)
    return table
    
def insertItems(setup,priceData, itemID):
    if (priceData[itemID]['low'] is None): ##if (priceData[itemID]['low'] is None):
        item_low = -1
    else:
        item_low = priceData[itemID]['low']
    
    if (priceData[itemID]['lowTime'] is None):
        item_low_time = -1
    else:
        item_low_time = datetime.fromtimestamp(priceData[itemID]['lowTime'])
    
    if (priceData[itemID]['high'] is None):
        item_hi = -1
    else:
        item_hi = priceData[itemID]['high']
        
    if (priceData[itemID]['highTime'] is None):
        item_hi_time = -1
    else:
        item_hi_time = datetime.fromtimestamp(priceData[itemID]['highTime'])
    
    values = (item_low, item_low_time, item_hi, item_hi_time)
    table = createTable(setup, itemID)
    if table == -1:
        return    
    sql_database.add_data(table, values)
    return table, values

def runScript(setup):
    priceData = getPrice()
    ## get all keys
    itemID = priceData['554']
    print(itemID)
    table, values = insertItems(setup, priceData, itemID)
    return table, values
    """
    for i in priceData.keys():
        itemID = str(i)
        table, values = insertItems(setup, priceData, itemID)
        return table, values
        
"""