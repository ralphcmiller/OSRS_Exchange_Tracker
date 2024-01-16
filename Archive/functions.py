# Description: This file contains the functions used in the main.py file.
# Date: 1/16/2023

# Formats API data into a readable format
def formatData(data):
    formatted_output = ""
    for key, values in data.items():
        formatted_output += f"Key: {key}\n"
        formatted_output += f"  High: {values['high']}, High Time: {values['highTime']}\n"
        formatted_output += f"  Low: {values['low']}, Low Time: {values['lowTime']}\n"
        formatted_output += "-" * 30 + "\n"
    return formatted_output

# returns the item info from an itemID
def getItemInfo(itemID):
    f = open('items.json')
    refrenceIDs = json.load(f)
    
    for i in refrenceIDs:
        if i == itemID:
            return refrenceIDs[i]