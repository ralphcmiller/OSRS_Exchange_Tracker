# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import json
import sql_database

from datetime import datetime
def changes(values):
    changes.value = values
def signalChange(color):
    signalChange.x = color
    
def getPrice():
    headers = {
        'User-Agent': 'Tracking Price Fluctuations',
        'From': 'Ralph#8350' 
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
    item_low = priceData[itemID]['low']
    item_low_time = (priceData[itemID]['lowTime']) #datetime.fromtimestamp
    item_hi = priceData[itemID]['high']
    item_hi_time = (priceData[itemID]['highTime'])
    
    values = (item_low, item_low_time, item_hi, item_hi_time)
    table = createTable(setup, itemID)
    
    if table == -1:
        return    
    
    sql_database.add_data(table, values)
    
    if changes.value != values:
        changes(values)
        color = 'green'
        signalChange(color)
    else:
        color = 'grey'
        signalChange(color)
        
    return table, values

def runScript(itemID, setup):
    priceData = getPrice()
    ## get all keys
    table, values = insertItems(setup, priceData, itemID)
    return table, values
    """
    for i in priceData.keys():
        itemID = str(i)
        table, values = insertItems(setup, priceData, itemID)
        return table, values
        
"""