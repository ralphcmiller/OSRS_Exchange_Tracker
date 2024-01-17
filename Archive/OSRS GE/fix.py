# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 22:52:08 2021

@author: ralph
"""
import json
def fixJson():
    f = open('items.json')
    refrenceIDs = json.load(f)
    f.close()
    
    for i in refrenceIDs:
        print(refrenceIDs[i])
        info = refrenceIDs[i]
        table = info['name'] 
        table = table.replace(" ", "_")
        table = table.replace("-", "_")
        table = table.replace("(", "")
        table = table.replace(")", "")
        table = table.replace("'", "")
        table = table.replace("&", "")
        table = table.replace(".", "")
        table = table.replace("+", "")
        table = table.replace("3", "thi")
        table = table.replace("/", "_")
        info['name'] = table
        refrenceIDs[i] = info
        print(refrenceIDs[i])
        
    f = open('items.json', 'w')
    json.dump(refrenceIDs, f)
    f.close()

    
fixJson()